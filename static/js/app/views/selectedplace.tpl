
    <td class="tdRelation">
        <% if (canRelate) { %>
        <a href="" class="relate">Relate</a>
        <% } %>
        <span class="makeRelation" style="display:none;">
            <select class="relationType">
                <option value="">does not relate to</option>
                <% for (r in relationChoices) { if (relationChoices.hasOwnProperty(r)) { var val = r; var rel = relationChoices[r]; %>
                    <option value="<%= val %>"><%= rel %></option>
                <% } } %>
            </select>
        </span>
    </td>
    <td class="tdName">
        <a href="<%= permalink %>"><%= properties.name %>
        <% if (display.admin) { %>
            <div class="adminDisplay"><%= display.admin %></div>
        <% } %>
        </a>
    </td>
    <td class="tdTimeframe">
        <%= display.timeframe %>
    </td>
    <td class="tdType">
        <%= display.feature_type %>
    </td>
    <td class="tdOrigin">
        <%= display.origin %>
    </td>
    <td class="tdRelateBtn">
        <% if (canRelate) { %>
            <span class="unselect">X</span>
        <% } else { %>
            <span class="unselect">X</span>
        <% } %>
    </td>
<!--
<h6><span class="smallestFont fontIcons">U</span><a href="" class="viewPlaceDetail"><strong><%= properties.name %></strong></a></h6>

<% if (display.admin) { %>
<p><span class="smallestFont fontIcons"></span> <%= display.admin %></p>

<% } %>

<% if (display.alternateNames) { %>
<p><span class="smallestFont fontIcons">J</span> <%=  display.alternateNames %></p>
<% } %>

<% if (display.timeframe) { %>
    <p><span class="smallestFont fontIcons">#</span> <%= display.timeframe %></p>
<% } %>

<p><span class="smallestFont fontIcons">_</span> <%= display.feature_type %></p>

<p><span class="smallestFont fontIcons">1</span> Origin: <a href="<%= originURL %>" target="_blank"><%= display.origin %></a></p>

<p class="resultsActions">
    <% if (hasGeometry) { %>
        <a href="" class="zoomOnMap">Zoom on map</a> / 
    <% } %>
    <a href="" class="viewPlaceDetail">View details</a> / 
    <a href="" class="unselect">Unselect</a><br />
    <div class="relateButtons">
        <% if (canRelate) { %>
            <a href="" class="relate">Relate</a>
        <% } else { %>
            <span>Please select 2 or more places to start relating.</span>
        <% } %>
        <a href="" class="stopRelate" style="display:none;">Done Relating</a>
    </div>
    <div class="makeRelation" style="display:none;">
        <span class="relatingFrom"></span>
        <select class="relationType">
            <option value="">does not relate to</option>
            <% for (r in relationChoices) { if (relationChoices.hasOwnProperty(r)) { var val = r; var rel = relationChoices[r]; %>
                <option value="<%= val %>"><%= rel %></option> 
            <% } } %>
        </select>
        this. <span class="confirmRelationBtn fontIcons" style="display:none;">*</span>
    </div>
</p>
-->
