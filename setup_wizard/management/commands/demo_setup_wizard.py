from django.core.management.base import BaseCommand
from setup_wizard.models import SetupProgress
from core.models import SiteSettings
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Demo and test the setup wizard functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset setup progress to start fresh',
        )
        parser.add_argument(
            '--complete-step',
            type=str,
            help='Mark a specific step as completed (e.g., site_info_completed)',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current setup status',
        )

    def handle(self, *args, **options):
        """Demo setup wizard functionality"""
        
        if options['reset']:
            self.reset_setup()
        elif options['complete_step']:
            self.complete_step(options['complete_step'])
        elif options['status']:
            self.show_status()
        else:
            self.show_help()
    
    def reset_setup(self):
        """Reset setup progress"""
        self.stdout.write("🔄 Resetting setup progress...")
        
        # Delete existing progress
        SetupProgress.objects.all().delete()
        
        # Create fresh progress
        progress = SetupProgress.get_progress()
        
        self.stdout.write(
            self.style.SUCCESS("✅ Setup progress reset successfully!")
        )
        self.show_status()
    
    def complete_step(self, step_key):
        """Mark a specific step as completed"""
        progress = SetupProgress.get_progress()
        
        if hasattr(progress, step_key):
            setattr(progress, step_key, True)
            progress.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Marked {step_key} as completed!")
            )
            self.show_status()
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ Unknown step: {step_key}")
            )
            self.stdout.write("Available steps:")
            for item in progress.get_all_items():
                self.stdout.write(f"  - {item['key']}")
    
    def show_status(self):
        """Show current setup status"""
        progress = SetupProgress.get_progress()
        
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("🚀 SETUP WIZARD STATUS"))
        self.stdout.write("="*60)
        
        # Overall progress
        overall_pct = progress.get_completion_percentage()
        essential_pct = progress.get_essential_completion_percentage()
        
        self.stdout.write(f"📊 Overall Progress: {overall_pct}%")
        self.stdout.write(f"⭐ Essential Progress: {essential_pct}%")
        self.stdout.write(f"✅ Essential Complete: {progress.is_essential_setup_complete()}")
        self.stdout.write(f"🎉 All Complete: {progress.is_setup_complete()}")
        
        # Essential items
        self.stdout.write("\n🔥 ESSENTIAL ITEMS:")
        for item in progress.get_essential_items():
            status = "✅" if item['completed'] else "❌"
            self.stdout.write(f"  {status} {item['icon']} {item['label']}")
        
        # Optional items
        self.stdout.write("\n💎 OPTIONAL ITEMS:")
        for item in progress.get_optional_items():
            status = "✅" if item['completed'] else "❌"
            self.stdout.write(f"  {status} {item['icon']} {item['label']}")
        
        # Next steps
        next_step = progress.get_next_step()
        if next_step:
            self.stdout.write(f"\n🎯 Next Step: {next_step['icon']} {next_step['label']}")
        else:
            self.stdout.write("\n🎉 No more steps - setup is complete!")
        
        # Metadata
        if progress.setup_started_at:
            self.stdout.write(f"\n📅 Started: {progress.setup_started_at}")
        if progress.setup_completed_at:
            self.stdout.write(f"🏁 Completed: {progress.setup_completed_at}")
        
        self.stdout.write("\n" + "="*60)
    
    def show_help(self):
        """Show usage examples"""
        self.stdout.write(self.style.SUCCESS("\n🚀 Setup Wizard Demo Commands:"))
        self.stdout.write("\n📊 Show current status:")
        self.stdout.write("  python manage.py demo_setup_wizard --status")
        
        self.stdout.write("\n🔄 Reset setup progress:")
        self.stdout.write("  python manage.py demo_setup_wizard --reset")
        
        self.stdout.write("\n✅ Complete a specific step:")
        self.stdout.write("  python manage.py demo_setup_wizard --complete-step site_info_completed")
        
        self.stdout.write("\n🌐 Available steps:")
        progress = SetupProgress.get_progress()
        for item in progress.get_all_items():
            self.stdout.write(f"  - {item['key']}")
        
        self.stdout.write("\n💡 URL endpoints:")
        self.stdout.write("  - Setup Wizard: /admin/setup/")
        self.stdout.write("  - Progress API: /admin/setup/api/progress/")
        self.stdout.write("  - Dashboard: /admin/ (shows setup widget)")
        
        self.stdout.write("\n🎯 Try the wizard:")
        self.stdout.write("  1. Run: python manage.py demo_setup_wizard --reset")
        self.stdout.write("  2. Visit: http://localhost:8000/admin/setup/")
        self.stdout.write("  3. Go through the wizard steps")
        self.stdout.write("  4. Check dashboard at: http://localhost:8000/admin/")
        
        self.stdout.write("")