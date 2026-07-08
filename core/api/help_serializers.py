"""
Help System API Serializers
DRF serializers for help system models
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.utils.translation import get_language, gettext_lazy as _
from core.models import HelpCategory, HelpTopic, HelpFeedback, HelpView


def _get_help_language(context=None):
    """Get the current language code for help translations.

    Checks for an explicit 'lang' query parameter first (used by the JS help
    panel since the API endpoint is outside i18n_patterns), then falls back
    to Django's get_language().
    Returns None if the language is English (default).
    """
    lang = None
    if context:
        request = context.get('request')
        if request:
            lang = request.query_params.get('lang')
    if not lang:
        lang = get_language()
    if not lang or lang == 'en' or lang.startswith('en-'):
        return None
    return lang


class HelpCategorySerializer(serializers.ModelSerializer):
    """Serializer for HelpCategory model"""

    topics_count = serializers.SerializerMethodField()

    class Meta:
        model = HelpCategory
        fields = [
            'id',
            'name',
            'slug',
            'icon',
            'order',
            'description',
            'topics_count',
        ]
        read_only_fields = ['id']

    @extend_schema_field(serializers.IntegerField())
    def get_topics_count(self, obj):
        """Get number of published topics in this category"""
        return obj.topics.filter(is_published=True).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = _get_help_language(self.context)
        if lang and instance.translations:
            lang_data = instance.translations.get(lang, {})
            if lang_data.get('name'):
                data['name'] = lang_data['name']
            if lang_data.get('description'):
                data['description'] = lang_data['description']
        return data


class HelpTopicListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing help topics"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    helpfulness_percentage = serializers.SerializerMethodField()

    class Meta:
        model = HelpTopic
        fields = [
            'id',
            'slug',
            'title_i18n_key',
            'category_name',
            'category_icon',
            'component',
            'view_count',
            'helpful_count',
            'not_helpful_count',
            'helpfulness_percentage',
            'updated_at',
        ]

    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_helpfulness_percentage(self, obj):
        """Get helpfulness percentage"""
        return obj.helpfulness_percentage

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = _get_help_language(self.context)
        if lang and instance.translations:
            lang_data = instance.translations.get(lang, {})
            if lang_data.get('title'):
                data['title_i18n_key'] = lang_data['title']
            # Category name translation
            if instance.category.translations:
                cat_lang = instance.category.translations.get(lang, {})
                if cat_lang.get('name'):
                    data['category_name'] = cat_lang['name']
        return data


class HelpTopicDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual help topic"""

    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    related_topics = serializers.SerializerMethodField()
    helpfulness_percentage = serializers.SerializerMethodField()

    class Meta:
        model = HelpTopic
        fields = [
            'id',
            'slug',
            'title_i18n_key',
            'category_name',
            'category_slug',
            'content_markdown',
            'component',
            'min_version',
            'max_version',
            'keywords',
            'url_patterns',
            'related_topics',
            'view_count',
            'helpful_count',
            'not_helpful_count',
            'helpfulness_percentage',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'view_count',
            'helpful_count',
            'not_helpful_count',
            'created_at',
            'updated_at',
        ]

    @extend_schema_field(HelpTopicListSerializer(many=True))
    def get_related_topics(self, obj):
        """Get related topics"""
        related = obj.related_topics.filter(is_published=True)
        return HelpTopicListSerializer(related, many=True, context=self.context).data

    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_helpfulness_percentage(self, obj):
        """Get helpfulness percentage"""
        return obj.helpfulness_percentage

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = _get_help_language(self.context)
        if lang and instance.translations:
            lang_data = instance.translations.get(lang, {})
            if lang_data.get('title'):
                data['title_i18n_key'] = lang_data['title']
            if lang_data.get('content'):
                data['content_markdown'] = lang_data['content']
            # Category name translation
            if instance.category.translations:
                cat_lang = instance.category.translations.get(lang, {})
                if cat_lang.get('name'):
                    data['category_name'] = cat_lang['name']
        return data


class HelpFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for submitting help feedback"""

    class Meta:
        model = HelpFeedback
        fields = [
            'id',
            'topic',
            'helpful',
            'comment',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create feedback and update topic counters"""
        # Set user from request if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user

        feedback = super().create(validated_data)

        # Update topic counters
        topic = feedback.topic
        if feedback.helpful:
            topic.helpful_count += 1
        else:
            topic.not_helpful_count += 1
        topic.save(update_fields=['helpful_count', 'not_helpful_count'])

        return feedback


class HelpSearchSerializer(serializers.Serializer):
    """Serializer for help search requests"""

    query = serializers.CharField(
        required=True,
        max_length=200,
        help_text=_("Search query")
    )
    component = serializers.CharField(
        required=False,
        max_length=50,
        help_text=_("Filter by component")
    )
    category = serializers.SlugField(
        required=False,
        help_text=_("Filter by category slug")
    )
    limit = serializers.IntegerField(
        required=False,
        default=10,
        min_value=1,
        max_value=50,
        help_text=_("Maximum number of results")
    )


class HelpSemanticSearchSerializer(serializers.Serializer):
    """Serializer for semantic search requests"""

    query = serializers.CharField(
        required=True,
        max_length=500,
        help_text=_("Natural language search query")
    )
    language = serializers.CharField(
        default='en',
        max_length=10,
        help_text=_("Language code for search (e.g., 'en', 'es', 'fr')")
    )
    component = serializers.CharField(
        required=False,
        max_length=50,
        help_text=_("Filter by component")
    )
    category = serializers.SlugField(
        required=False,
        help_text=_("Filter by category slug")
    )
    limit = serializers.IntegerField(
        default=10,
        min_value=1,
        max_value=50,
        help_text=_("Maximum number of results")
    )
    threshold = serializers.FloatField(
        default=0.4,
        min_value=0.0,
        max_value=2.0,
        help_text=_("Similarity threshold (0-2, lower = more similar)")
    )


class HelpContextSerializer(serializers.Serializer):
    """Serializer for context-aware help requests"""

    url_path = serializers.CharField(
        required=True,
        max_length=500,
        help_text=_("Current page URL path (e.g., /admin/catalog/products/)")
    )
    component = serializers.CharField(
        required=False,
        max_length=50,
        help_text=_("Current component context")
    )
    limit = serializers.IntegerField(
        required=False,
        default=5,
        min_value=1,
        max_value=20,
        help_text=_("Maximum number of suggestions")
    )


# Admin Metadata API Serializers

class AdminTemplatesSerializer(serializers.Serializer):
    """Serializer for ModelAdmin template configurations"""

    change_form_template = serializers.CharField(allow_null=True, required=False)
    change_list_template = serializers.CharField(allow_null=True, required=False)
    delete_confirmation_template = serializers.CharField(allow_null=True, required=False)
    object_history_template = serializers.CharField(allow_null=True, required=False)


class AdminListConfigurationSerializer(serializers.Serializer):
    """Serializer for ModelAdmin list view configuration"""

    list_display = serializers.ListField(child=serializers.CharField())
    list_filter = serializers.ListField(child=serializers.CharField())
    search_fields = serializers.ListField(child=serializers.CharField())
    ordering = serializers.ListField(child=serializers.CharField())
    date_hierarchy = serializers.CharField(allow_null=True, required=False)


class AdminFieldsetSerializer(serializers.Serializer):
    """Serializer for individual fieldset in ModelAdmin"""

    name = serializers.CharField(allow_null=True)
    fields = serializers.ListField(child=serializers.CharField())
    classes = serializers.ListField(child=serializers.CharField())
    description = serializers.CharField(allow_blank=True)


class AdminFormConfigurationSerializer(serializers.Serializer):
    """Serializer for ModelAdmin form configuration"""

    fieldsets = AdminFieldsetSerializer(many=True)
    readonly_fields = serializers.ListField(child=serializers.CharField())
    custom_form = serializers.CharField(allow_null=True, required=False)
    form_module = serializers.CharField(allow_null=True, required=False)


class AdminInlineSerializer(serializers.Serializer):
    """Serializer for ModelAdmin inline formsets"""

    inline_class = serializers.CharField(source='class')
    model = serializers.CharField(allow_null=True, required=False)
    extra = serializers.IntegerField()
    max_num = serializers.IntegerField(allow_null=True, required=False)
    min_num = serializers.IntegerField(allow_null=True, required=False)


class AdminMediaSerializer(serializers.Serializer):
    """Serializer for ModelAdmin Media (JS/CSS)"""

    js = serializers.ListField(child=serializers.CharField())
    css = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))


class AdminFlagsSerializer(serializers.Serializer):
    """Serializer for ModelAdmin feature flags"""

    has_custom_change_form = serializers.BooleanField()
    has_custom_change_list = serializers.BooleanField()
    has_custom_media = serializers.BooleanField()
    has_fieldsets = serializers.BooleanField()
    has_inlines = serializers.BooleanField()


class AdminModelMetadataSerializer(serializers.Serializer):
    """Serializer for complete ModelAdmin metadata"""

    app_label = serializers.CharField()
    model_name = serializers.CharField()
    verbose_name = serializers.CharField()
    verbose_name_plural = serializers.CharField()
    admin_class = serializers.CharField()
    templates = AdminTemplatesSerializer()
    list_configuration = AdminListConfigurationSerializer()
    form_configuration = AdminFormConfigurationSerializer()
    inlines = AdminInlineSerializer(many=True)
    custom_actions = serializers.ListField(child=serializers.CharField())
    media = AdminMediaSerializer(allow_null=True, required=False)
    flags = AdminFlagsSerializer()


class AdminMetadataResponseSerializer(serializers.Serializer):
    """Serializer for the complete admin metadata API response"""

    timestamp = serializers.DateTimeField()
    count = serializers.IntegerField()
    models = AdminModelMetadataSerializer(many=True)
