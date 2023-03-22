/*
    HTML element ids
*/
const EDIT_USERNAME_BUTTON = "#editusernamebtn";
const USERNAME_BOX = "#usernamebox";
const EDIT_USERNAME_BOX = "#usernamebox-edit"
const SAVE_USERNAME_BUTTON = "#saveusernamebtn";
const USERNAME_TEXT = "#usernametext";
const USERNAME_TEXT_UPDATING = "#usernametext-updating";

/*
    Changes the page for when the username is updating
    Username display is set to the updating message
    Edit button is disabled
*/
function toggleUsernameUpdating(updating) {
    if (updating) {
        $(USERNAME_TEXT).hide();
        $(USERNAME_TEXT_UPDATING).show();
        $(EDIT_USERNAME_BUTTON).attr('disabled', true);
    }
    else {
        $(USERNAME_TEXT).show();
        $(USERNAME_TEXT_UPDATING).hide();
        $(EDIT_USERNAME_BUTTON).attr('disabled', false);
    }
}

/*
    Changes whether the username display or editor is shown
*/
function toggleUsernameEdit(editing) {
    if (editing) {
        // Hide display
        $(USERNAME_BOX).hide();
        $(EDIT_USERNAME_BUTTON).hide()

        // Show input
        $(EDIT_USERNAME_BOX).show();
        $(SAVE_USERNAME_BUTTON).show();
    }
    else {
        // Show display
        $(USERNAME_BOX).show();
        $(EDIT_USERNAME_BUTTON).show();

        // Hide input
        $(EDIT_USERNAME_BOX).hide();
        $(SAVE_USERNAME_BUTTON).hide();
    }
}

$(document).ready(function() {
    // Hide editing and updating elements
    toggleUsernameEdit(false);
    toggleUsernameUpdating(false);

    $(EDIT_USERNAME_BUTTON).click(function() {
        // Show editing elements
        toggleUsernameEdit(true);

        // Update name in input
        $(EDIT_USERNAME_BOX).val($(USERNAME_TEXT).html());
    });

    $(SAVE_USERNAME_BUTTON).click(function() {
        // Hide editing elements
        toggleUsernameEdit(false);

        // Handle new name
        before = $(USERNAME_TEXT).html();
        after = $(EDIT_USERNAME_BOX).val();
        if (before != after) {
            // Disable edit button until response is received
            toggleUsernameUpdating(true);

            // Request update
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    // Notify user
                    var msg = this.responseText;
                    if (this.status != 200 && this.status != 403 && this.status != 406) {
                        msg = "Error " + this.status + ": " + this.responseText;
                    }
                    alert(msg);

                    // Update text if successful and display
                    if (this.status == 200) {
                        $(USERNAME_TEXT).html($(EDIT_USERNAME_BOX).val());
                    }

                    // Re-enable button
                    toggleUsernameUpdating(false);
                }
            }
            xhttp.open("POST", "/gsr/edit_user/", true);
            xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("name="+after);
        }
    });
});
