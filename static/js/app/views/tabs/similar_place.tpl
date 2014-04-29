    <td class="tdRelation">
        <span class="relationText">
            No relation
        </span>
        <span class="editable">
            <select class="relationSelect">
                <option value="">does not relate to</option>
                <% for (r in relationChoices) { if (relationChoices.hasOwnProperty(r)) { var val = r; var rel = relationChoices[r]; %>
                    <option value="<%= val %>"><%= rel %></option>
                <% } } %>
            </select>
        </span>
    
    </td>
    <td class="tdName">
        <a href="<%= permalink %>">
        <%= properties.name %>
        <% if (display.admin) { %>
            <div class="adminDisplay"><%= display.admin %></div>
        <% } %>
        </a>
    </td>
    <td class="tdTimeframe">
        <%= display.timeframe %>
    </td>
    <td class="tdType">
        <%= properties.feature_code %>
    </td>

