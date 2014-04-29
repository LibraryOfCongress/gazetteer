<form action="" class="formModal" id="relatePlacesForm">
    <h6 class="serif">Make a Relation</h6>
    <br>

    <div class="marginBottom relationDetails">
         <%= place1_name %><br />
         <%= relation %><br />
         <%= place2_name %> 
    </div>
    <div class="marginBottom">
        <label for="revertComments">Comments:</label> <textarea placeholder="Comments about your changes." class="comments" id="relateComments"></textarea>
    </div>

    <div class="marginBottom">
    <input type="submit" value="Submit" class="button" />
    </div>

    <div class="message"></div>
</form>
