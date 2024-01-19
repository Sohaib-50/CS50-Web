function formatText(style) {
    var editor = document.getElementById('editor');

    // Get the selection range
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);

    // Create a new element based on the chosen style
    var newElement;
    switch (style) {
        case 'bold':
            newElement = document.createElement('b');
            break;
        case 'normal':
            newElement = document.createElement('span');
            break;
        case 'h1':
            newElement = document.createElement('h1');
            break;
        case 'h2':
            newElement = document.createElement('h2');
            break;
    }

    // Wrap the selected range with the new element
    range.surroundContents(newElement);

    // Clear the selection
    selection.removeAllRanges();
}

// You can add more functions for additional formatting options as needed
