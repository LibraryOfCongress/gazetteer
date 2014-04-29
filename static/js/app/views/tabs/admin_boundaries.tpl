<p class="smallFont"><strong>
    <% if (url) { %>
    <a href="<%= url %>" class="openPlace">
    <% } %>
        <%= name %>
    <% if (url) { %>
    </a>
    <% } %>
</strong></p>
<p class="smallFont"><%= alternate_names %></p>
<p class="smallFont"><%= feature_code %></p>
