---
layout: page
title: Archive
permalink: /archive/
---

# Post Archive

Browse all posts organized by date and category.

## Posts by Year

{% assign postsByYear = site.posts | group_by_exp: 'post', 'post.date | date: "%Y"' %}
{% for year in postsByYear %}

## {{ year.name }}

<div class="archive-year">
{% assign postsByMonth = year.items | group_by_exp: 'post', 'post.date | date: "%B"' %}
{% for month in postsByMonth %}

### {{ month.name }} {{ year.name }}

<div class="archive-month">
{% for post in month.items %}
<div class="archive-post">
  <span class="archive-date">{{ post.date | date: "%d" }}</span>
  <a href="{{ post.url | relative_url }}" class="archive-title">{{ post.title }}</a>
  {% if post.categories.size > 0 %}
    <span class="archive-categories">
      {% for category in post.categories %}
        <a href="{{ '/category/' | append: category | relative_url }}" class="archive-category">{{ category }}</a>{% unless forloop.last %}, {% endunless %}
      {% endfor %}
    </span>
  {% endif %}
</div>
{% endfor %}
</div>

{% endfor %}
</div>

{% endfor %}

## Browse by Category

<div class="archive-categories-list">
{% for category in site.categories %}
  <div class="category-archive-item">
    <h3><a href="{{ '/category/' | append: category[0] | relative_url }}">{{ category[0] | capitalize }}</a></h3>
    <p>{{ category[1].size }} posts</p>
    <ul class="category-posts-list">
    {% for post in category[1] limit:5 %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
    {% if category[1].size > 5 %}
      <li><a href="{{ '/category/' | append: category[0] | relative_url }}">View all {{ category[1].size }} posts...</a></li>
    {% endif %}
    </ul>
  </div>
{% endfor %}
</div>

## Search Posts

Use our [search feature]({{ '/search/' | relative_url }}) to quickly find specific content.

<style>
.archive-year {
  margin-bottom: 2rem;
}

.archive-month {
  margin-bottom: 1.5rem;
  margin-left: 1rem;
}

.archive-post {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  gap: 1rem;
}

.archive-date {
  font-weight: bold;
  color: var(--meta-color);
  min-width: 2rem;
}

.archive-title {
  flex: 1;
  text-decoration: none;
  color: var(--link-color);
}

.archive-title:hover {
  text-decoration: underline;
}

.archive-categories {
  font-size: 0.9rem;
  color: var(--meta-color);
}

.archive-category {
  color: var(--link-color);
  text-decoration: none;
}

.archive-category:hover {
  text-decoration: underline;
}

.archive-categories-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.category-archive-item {
  background: var(--card-bg);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
}

.category-archive-item h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.category-archive-item p {
  color: var(--meta-color);
  margin-bottom: 1rem;
}

.category-posts-list {
  list-style: none;
  padding: 0;
}

.category-posts-list li {
  margin-bottom: 0.25rem;
}

.category-posts-list a {
  color: var(--text-color);
  text-decoration: none;
  font-size: 0.9rem;
}

.category-posts-list a:hover {
  color: var(--link-color);
}
</style>