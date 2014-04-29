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
        <%= display.feature_type %>
    </td>
    <td class="tdOrigin">
        <%= display.origin %>
    </td>
    <td class="tdIcons">
        <span class="actionIcons" style="display:none;">
            <!-- <span class="viewPlaceDetail fontIcons">. <span class="tooltip"> View Place Detail </span></span>
            <span class="editPlaceDetail fontIcons" style="display:none;">) <span class="tooltip"> Edit Place </span></span>
            <span class="zoomOnMap fontIcons">/ <span class="tooltip">Zoom on Map</span></span> -->
            <span class="selectBtns" style="display:none;">
                <span class="selectPlace fontIcons">0<span class="tooltip"> Select Place </span></span>
                <span class="unselectPlace fontIcons" style="display:none;">3</span>
            </span>
        </span>    
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
    <a href="" class="selectPlace">Select</a>
    <a href="" class="unselectPlace" style="display:none;">Unselect</a>
</p>
-->
