<h3>Application Error</h3>
<p>
    Status Code: <%= statusCode %><br />
    Error accessing <a href="<%= errorUrl %>" target="_blank"><%= errorUrl %></a> <br /><br />
    <% if (errorMsg) { %>
        Error: <%= errorMsg %>
    <% } %>

</p>
