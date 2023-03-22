/*
    HTML element ids
*/
const USERNAME_BOX = "#usernamebox";
const USERNAME_TEXT = "#usernametext";
const USERNAME_TEXT_UPDATING = "#usernametext-updating";
const EDIT_USERNAME_BUTTON = "#editusernamebtn";
const EDIT_USERNAME_BOX = "#usernamebox-edit"
const SAVE_USERNAME_BUTTON = "#saveusernamebtn";

const EMAIL_BOX = "#emailbox";
const EMAIL_TEXT = "#emailtext";
const EMAIL_TEXT_UPDATING = "#emailtext-updating"
const EDIT_EMAIL_BUTTON = "#editemailbtn"
const EDIT_EMAIL_BOX = "#emailbox-edit";
const SAVE_EMAIL_BUTTON = "#saveemailbtn"

/*
    Context format:
            == Display mode ==
        display_box - main box that the value is displayed in
        display_text - span containing the raw value text
        updating_text - span containing the updating message
        edit_btn - button to start editing

            == Edit mode ==
        edit_box - input box when editing
        save_btn - button to end editing

            == AJAX ==
        post_name - name to use for post parameter
*/

username_edit_ctx = {
    'display_box' : USERNAME_BOX,
    'display_text' : USERNAME_TEXT,
    'updating_text' : USERNAME_TEXT_UPDATING,
    'edit_btn' : EDIT_USERNAME_BUTTON,

    'edit_box' : EDIT_USERNAME_BOX,
    'save_btn' : SAVE_USERNAME_BUTTON,

    'post_name' : 'name',
};

email_edit_ctx = {
    'display_box' : EMAIL_BOX,
    'display_text' : EMAIL_TEXT,
    'updating_text' : EMAIL_TEXT_UPDATING,
    'edit_btn' : EDIT_EMAIL_BUTTON,

    'edit_box' : EDIT_EMAIL_BOX,
    'save_btn' : SAVE_EMAIL_BUTTON,

    'post_name' : 'email',
};

/*
    Hides the value and shows the updating message if needed
*/
function toggleUpdating(ctx, updating) {
    if (updating) {
        $(ctx.display_text).hide();
        $(ctx.updating_text).show();
        $(ctx.edit_btn).attr('disabled', true);
    }
    else {
        $(ctx.display_text).show();
        $(ctx.updating_text).hide();
        $(ctx.edit_btn).attr('disabled', false);
    }
}

/*
    Changes whether the value display or editor is shown
*/
function toggleEditing(ctx, editing) {
    if (editing) {
        // Hide display
        $(ctx.display_box).hide();
        $(ctx.edit_btn).hide()

        // Show input
        $(ctx.edit_box).show();
        $(ctx.save_btn).show();
    }
    else {
        // Show display
        $(ctx.display_box).show();
        $(ctx.edit_btn).show();

        // Hide input
        $(ctx.edit_box).hide();
        $(ctx.save_btn).hide();
    }
}

/*
    Gets the user input
*/
function getInput(ctx) {
    return $(ctx.edit_box).val();
}

/*
    Pre-sets the input box
*/
function setInput(ctx, val) {
    $(ctx.edit_box).val(val);
}

/*
    Gets the displayed value
*/
function getDisplay(ctx) {
    return $(ctx.display_text).html();
}

/*
    Sets the displayed value
*/
function setDisplay(ctx, val) {
    $(ctx.display_text).html(val);
}

function setupEditor(ctx) {
    // Hide editing and updating elements
    toggleEditing(ctx, false);
    toggleUpdating(ctx, false);

    // Switch to editor on edit button press
    $(ctx.edit_btn).click(function() {
        // Show editing elements
        toggleEditing(ctx, true);

        // Update name in input
        var display = getDisplay(ctx);
        setInput(ctx, display);
    });

    // Switch back to display when save button pressed, try tell server
    $(ctx.save_btn).click(function() {
        // Hide editing elements
        toggleEditing(ctx, false);

        // Handle new name
        var before = getDisplay(ctx);
        var after = getInput(ctx);
        if (before != after) {
            // Disable edit button until response is received
            toggleUpdating(ctx, true);

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
                        var input = getInput(ctx);
                        setDisplay(ctx, input);
                    }

                    // Re-enable button
                    toggleUpdating(ctx, false);
                }
            }
            xhttp.open("POST", "/gsr/edit_user/", true);
            xhttp.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send(ctx.post_name + "=" + after);
        }
    });
}

$(document).ready(function() {
    setupEditor(username_edit_ctx);
    setupEditor(email_edit_ctx);
});
