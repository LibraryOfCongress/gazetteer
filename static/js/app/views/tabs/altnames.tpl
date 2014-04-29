<div class="altnameDetails">
    <p class="smallFont">
        <strong>
            <span class="altnameDetail alternateNameName"><%= name %></span>
        </strong>
        <span class="altnameEditable">
		<span class="labelAltNames">Alt Name: </span>
		<input type="text" class="alternateNameNameInput" value="<%= name %>" placeholder="Alternate Name" />
        </span>
    </p>
    <p class="smallFont">
        <span class="labelAltNames">Language: </span>
        <span class="altnameDetail alternateNameLang"><%= lang %></span>
        <span class="altnameEditable">
            <input class="alternateNameLangInput" type="text" value="<%= lang %>" placeholder="Language" />    
        </span>
    </p>
    <p class="smallFont">
        <span class="labelAltNames">Type: </span>
        <span class="altnameDetail alternateNameType"><%= type %></span>
        <span class="altnameEditable">
            <input class="alternateNameTypeInput" type="text" value="<%= type %>" placeholder="Type" />
        </span>
    </p>
    <div class="editButtons">
        <p class="editAlternateName buttonAdd inlineBlock">Edit <span class="fontIcons buttonAddIcon"> )</span></p>
        <p class="deleteAlternateName buttonAdd inlineBlock">Delete<span class="smallFont buttonAddIcon"><strong> x</strong></span></p>
    </div>
    <div class="saveButtons" style="display:none;">
        <span class="labelAltNames">&nbsp;</span>
        <p class="saveAlternateName buttonAdd inlineBlock">Save <span class="fontIcons buttonAddIcon ">0</span></p>
        <p class="cancel buttonAdd inlineBlock">Cancel <span class="fontIcons buttonAddIcon ">4</span></p> 
    </div>
</div>
