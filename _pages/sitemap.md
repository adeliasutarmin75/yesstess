---
layout: page
title: Sitemap
permalink: /sitemap/
---

# Sitemap

Welcome to our website sitemap. This page provides a comprehensive overview of all the content available on {{ site.title }}.

## Main Pages

- [Home]({{ '/' | relative_url }}) - Latest posts and featured content
- [About]({{ '/about/' | relative_url }}) - Learn more about us
- [Contact]({{ '/contact/' | relative_url }}) - Get in touch with us
- [Documentation]({{ '/documentation/' | relative_url }}) - Technical documentation and guides

## Legal Pages

- [Privacy Policy]({{ '/privacy-policy/' | relative_url }}) - How we handle your data
- [Disclaimer]({{ '/disclaimer/' | relative_url }}) - Important legal information  
- [Terms of Service]({{ '/terms-of-service/' | relative_url }}) - Terms and conditions
- [Cookie Policy]({{ '/cookie-policy/' | relative_url }}) - Information about cookies

## Categories

{% for category in site.categories %}
- [{{ category[0] | capitalize }}]({{ '/category/' | append: category[0] | relative_url }}) ({{ category[1].size }} posts)
{% endfor %}

## Tags

{% assign tags = site.tags | sort %}
{% for tag in tags %}
- [{{ tag[0] }}]({{ '/tag/' | append: tag[0] | relative_url }}) ({{ tag[1].size }} posts)
{% endfor %}

## Recent Posts

{% for post in site.posts limit:10 %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

## All Posts by Date

{% assign postsByYear = site.posts | group_by_exp: 'post', 'post.date | date: "%Y"' %}
{% for year in postsByYear %}

### {{ year.name }}

{% for post in year.items %}
- {{ post.date | date: "%m/%d" }} - [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}

{% endfor %}

## Search

Looking for something specific? Use our [search feature]({{ '/search/' | relative_url }}) to find content quickly.

---

**Last updated:** {{ site.time | date: "%B %d, %Y at %I:%M %p %Z" }}

For technical issues or questions, please [contact us]({{ '/contact/' | relative_url }}).