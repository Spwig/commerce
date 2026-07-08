---
slug: blog-management
title_i18n_key: Blog Management
category: design-content
component: blog
keywords:
  - blog
  - blog post
  - blog category
  - blog tag
  - subscriber
  - newsletter
  - social media
  - auto share
  - RSS
  - content marketing
url_patterns:
  - /admin/blog/blogpost/
  - /admin/blog/blogcategory/
  - /admin/blog/blogsubscriber/
related:
  - store-settings
published: true
---

The blog lets you publish articles, guides, and news to drive traffic and engage your audience. Spwig's blog includes a rich text editor, scheduled publishing, subscriber notifications, automatic social media sharing, and SEO tools.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Creating a Blog Post

Navigate to **Marketing > Blog Posts** and click **Add Post**.

### Post Content

Write your post using the **CKEditor 5** rich text editor, which supports:
- Text formatting (headings, bold, italic, lists, blockquotes)
- Images and media (uploaded through the media library)
- Embedded videos (YouTube, Vimeo)
- Tables and code blocks
- Links to products, categories, and external URLs

For more complex layouts, enable the **Page Builder** toggle to use the drag-and-drop page builder instead of the text editor.

### Post Settings

| Setting | Description |
|---------|-------------|
| **Title** | The headline displayed on the blog and in search results |
| **Slug** | URL-friendly identifier (auto-generated from title, editable) |
| **Excerpt** | Short summary shown in blog listing cards and RSS feeds |
| **Featured Image** | Main image displayed at the top of the post and in listing cards |
| **Category** | Primary category for the post |
| **Tags** | Keywords for filtering and related content |
| **Author** | Staff member credited as the author |
| **Status** | Draft, Scheduled, Published, or Archived |
| **Featured** | Pin the post to the top of the blog listing |

### SEO Settings

Each post includes SEO fields:
- **Meta Title** — Custom title for search engine results (defaults to post title)
- **Meta Description** — Summary shown in search engine results
- **Open Graph Image** — Image used when the post is shared on social media

## Post Statuses

| Status | Description |
|--------|-------------|
| **Draft** | Work in progress, not visible to the public |
| **Scheduled** | Will be automatically published at a set date and time |
| **Published** | Live and visible to visitors |
| **Archived** | Hidden from the blog listing but still accessible via direct URL |

### Scheduling Posts

To schedule a post for future publication:
1. Set the status to **Scheduled**
2. Choose the **publish date and time**
3. Save the post

A background task automatically publishes the post at the scheduled time and triggers subscriber notifications.

## Categories

Navigate to **Marketing > Blog Categories** to organize your content.

Categories support:
- **Hierarchy** — Create parent and child categories (e.g., "Guides" > "Getting Started")
- **Custom URLs** — Each category has its own slug for clean URLs
- **Descriptions** — Add category descriptions shown on the category archive page
- **Ordering** — Control the display order of categories in navigation

## Tags

Tags provide a secondary way to classify content. Unlike categories (which are hierarchical), tags are flat labels. Visitors can click a tag to see all posts with that tag.

## Subscribers

Navigate to **Marketing > Blog Subscribers** to manage your subscriber list.

### How Subscriptions Work

1. Visitors subscribe via a form on the blog (email address required)
2. A **double opt-in** confirmation email is sent
3. Once confirmed, the subscriber receives notifications when new posts are published

### Notification Frequency

Subscribers choose how often they receive notifications:

| Frequency | Description |
|-----------|-------------|
| **Immediate** | Email sent as soon as a new post is published |
| **Weekly Digest** | A weekly summary of all new posts |
| **Monthly Digest** | A monthly summary of all new posts |

Background tasks handle digest compilation and delivery automatically.

### Managing Subscribers

- View subscriber count, confirmation status, and signup date
- Export subscriber lists for use in external email marketing tools
- Remove or unsubscribe individual addresses
- Each notification email includes a one-click **unsubscribe link**

## Social Media Auto-Sharing

Spwig can automatically share new posts to your social media accounts when they are published.

### Connecting Social Accounts

Navigate to **Marketing > Social Connectors** to connect your accounts:

| Platform | Authentication |
|----------|---------------|
| **Facebook** | OAuth — connect your Facebook Page |
| **Instagram** | OAuth — connect your business account |
| **LinkedIn** | OAuth — connect your company page |

### How Auto-Sharing Works

1. Connect one or more social accounts
2. When creating a post, enable **Auto Share** for each connected account
3. Customize the share message (defaults to the post title and excerpt)
4. When the post is published (or reaches its scheduled time), it is automatically shared

Auto-sharing also works with scheduled posts — the social share is sent at the same time the post goes live.

## RSS Feed

The blog automatically generates an RSS feed at `/blog/feed/`. This allows visitors and aggregators to subscribe to your content. The feed includes:
- Post title and excerpt
- Publication date
- Author information
- Direct link to the full post

## Blog Settings

Navigate to **Marketing > Blog Settings** to configure global blog options:

- **Posts Per Page** — Number of posts shown per page in the listing
- **Allow Comments** — Enable or disable commenting on posts
- **Default Category** — Fallback category for posts without one assigned
- **Social Sharing Buttons** — Show share buttons on individual post pages

## Tips

- Write posts with **SEO in mind** — use descriptive titles, fill in meta descriptions, and include relevant keywords naturally in the content.
- Use **scheduled publishing** to maintain a consistent posting cadence without manual effort.
- Enable **auto-sharing** to maximize reach — posts shared on social media shortly after publication get the most engagement.
- Encourage visitors to **subscribe** by placing the subscription form prominently on your blog and using a compelling call to action.
- Use **categories** for broad content groupings and **tags** for specific topics — this helps visitors find related content.
- Add a **featured image** to every post — posts with images perform better in search results and social media shares.
- Use the **weekly or monthly digest** option for subscribers who don't want frequent emails — it reduces unsubscribe rates.
