TocTypeEnum = {
  VERTICAL: 1,
  HORIZONTAL: 2
};

function CreateTOC(tocElement) {

  // Find the toc element DIV. We'll place our TOC there.
  var toc = document.getElementById(tocElement);

  var tocTypeClass = toc.className;
  var tocType;

  switch (tocTypeClass) {
      case 'horizontal_toc':
        tocType = TocTypeEnum.HORIZONTAL;
        break;
      case 'vertical_toc':
        tocType = TocTypeEnum.VERTICAL;
        break;
      default:
        tocType = TocTypeEnum.VERTICAL;
        break;
  }

  // If toc_levels is defined, set headingLevels to it.
  // Otherwise, use default value of "h2,h3"
  var headingLevels;
  if (typeof toc_levels === 'undefined') {
    headingLevels = 'h2,h3';
  } else {

  }

  // Collect all section heading elements in an array
  var headings = document.querySelectorAll(headingLevels);

  // Add TOC title elements
  var tocHeadingDiv = document.createElement('div');
  toc.appendChild(tocHeadingDiv);
  tocHeadingDiv.className = 'toc_title';
  var tocHeading = document.createElement('h3');
  toc.appendChild(tocHeading);
  tocHeading.className = 'ignoreLink';
  tocHeading.id = 'toc';
  var tocText = document.createTextNode('Table of Contents');
  tocHeading.appendChild(tocText);

  // Add table and tbody
  var tocTable = document.createElement('table');
  if (tocType == TocTypeEnum.VERTICAL) {
    tocTable.className = 'columns';
  }
  toc.appendChild(tocTable);

  var tbody_element = document.createElement('tbody');
  tbody_element.setAttribute('valign', 'top');
  tbody_element.className = 'toc';
  tocTable.appendChild(tbody_element);

  // Get the highest level heading
  var firstHeading = headings[0];
  var masterLevel = parseInt(headingLevels.charAt(1));

  // Get the lowest heading level
  var lowestLevel = parseInt(headingLevels.charAt(headingLevels - 1));

  switch (tocType) {
    case TocTypeEnum.HORIZONTAL:
        CreateHorizontalTOC(headings, masterLevel, lowestLevel, tbody_element);
        break;
    case TocTypeEnum.VERTICAL:
        CreateVerticalTOC(headings, masterLevel, lowestLevel, tbody_element);
        break;
    default:
   }
}

function CreateHorizontalTOC(
             headings, masterLevel, lowestLevel, tbody_element) {

  // Initialize the header counter
  var h = 0;
  var ignoreChildren = false;

  while (h < headings.length) {
    // Get current heading
    var heading = headings[h];

    // Get the current heading level
    var level = parseInt(heading.tagName.charAt(1));

    if (isNaN(level) || level < 1 || level > lowestLevel) continue;

    // If level is a masterLevel, make it a TOC parent category
    if ((level == masterLevel) && (!hasClass(heading, 'ignoreLink'))) {
      toc_current_row = AddTOCMaster(tbody_element, heading);
      ignoreChildren = false;
    }

    if ((level == masterLevel) && (hasClass(heading, 'ignoreLink'))) {
      ignoreChildren = true;
    }

    if ((level != masterLevel) && (!ignoreChildren)) {
      AddTOCElements(toc_current_row, heading);
    }

    // Advance the header counter
    h++;
  }
}

// Adds a master Table of Content heading
function AddTOCMaster(tocTable, heading) {

  // Add the table row scaffolding
  var toc_tr = document.createElement('tr');
  tocTable.appendChild(toc_tr);
  toc_tr.setAttribute('valign', 'top');
  var toc_tr_td = document.createElement('td');
  toc_tr.appendChild(toc_tr_td);
  var toc_category = document.createElement('div');
  toc_tr_td.appendChild(toc_category);
  toc_category.className = 'toc_category';

  // Create the link to this header
  var link = document.createElement('a');
  link.href = '#' + heading.id;       // Create the anchor link
  link.textContent = heading.textContent; // Link text is same as heading
  toc_category.appendChild(link);

  // Add the container table cell for its children
  var toc_td = document.createElement('td');
  toc_tr.appendChild(toc_td);
  var toc_td_div = document.createElement('div');
  toc_td_div.className = 'toc_stylepoint';
  toc_td.appendChild(toc_td_div);

  return (toc_td_div);
}

// Adds Table of Contents element to a master heading as children
function AddTOCElements(toc_div, heading) {

  if (heading.offsetParent === null) {
    // The element is currently hidden, so don't create a TOC entry
  } else {
    // Create the list item element
    var toc_list_element = document.createElement('li');
    toc_list_element.className = 'toc_entry';
    toc_div.appendChild(toc_list_element);

    // Create the link to this header
    var link = document.createElement('a');
    link.href = '#' + heading.id;       // Create the anchor link
    link.textContent = heading.textContent; // Link text is same as heading
    toc_list_element.appendChild(link);
  }
}

function CreateVerticalTOC(headings, masterLevel, lowestLevel, tbody_element) {

  // Create the Column scaffolding
  var toc_tr = document.createElement('tr');
  tbody_element.appendChild(toc_tr);
  var toc_tr_td = document.createElement('td');
  toc_tr_td.className = 'two_columns';
  toc_tr.appendChild(toc_tr_td);


  // Initialize the header counter and the current row
  var h = 0;
  var toc_current_col = null;
  var ignoreChildren = false;

  while (h < headings.length) {
    // Get current heading
    var heading = headings[h];

    // Get the current heading level
    var level = parseInt(heading.tagName.charAt(1));

    if (isNaN(level) || level < 1 || level > lowestLevel) continue;

    // If level is a masterLevel, make it a TOC parent category
    if ((level == masterLevel) && (!hasClass(heading, 'ignoreLink'))) {
      if (heading.offsetParent === null) {
        // The element is currently hidden, so don't create a TOC entry
      } else {
        var td_dl = document.createElement('dl');
        toc_tr_td.appendChild(td_dl);
        var td_dt = document.createElement('dt');
        td_dl.appendChild(td_dt);
        toc_current_col = td_dl;

        // Create the link to this header
        var link = document.createElement('a');
        link.href = '#' + heading.id;       // Create the anchor link
        link.textContent = heading.textContent; // Link text is same as heading
        td_dt.appendChild(link);
        ignoreChildren = false;
      }
    }

    // If level is a masterLevel but it's specified to ignore links, skip it
    // and its children.
    if ((level == masterLevel) && (hasClass(heading, 'ignoreLink'))) {
      ignoreChildren = true;
    }

    if ((level != masterLevel) && (!ignoreChildren)) {
      if (heading.offsetParent === null) {
        // The element is currently hidden, so don't create a TOC entry
      } else {
        var td_dd = document.createElement('dd');
        toc_current_col.appendChild(td_dd);
        // Create the link to this header
        var link = document.createElement('a');
        link.href = '#' + heading.id;       // Create the anchor link
        link.textContent = heading.textContent; // Link text is same as heading
        td_dd.appendChild(link);
      }
    }

    // Advance the header counter
    h++;
  }
}

/*
 * Utility function for finding elements with a given
 * class.
 */
function hasClass(element, cls) {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
}

/*
 * Linkify all h2 through h4 headers, except for those marked
 * "ignoreLink"
 */

// Add the link image to the element.
function LinkifyHeader(header, fileName, sizePixels) {
  var link = document.createElement('a');
  link.href = '#' + header.id;
  link.alt = 'link to ' + header.id;
  link.innerHTML =
      '<img src="include/' + fileName + '"' +
      ' width=' + sizePixels +
      ' height=' + sizePixels +
      ' style="float:left;position:relative;bottom:5px;">';
  header.appendChild(link);
}

// Find all elements of the given tag and linkify if
// they don't have 'ignoreLink' in their class.
function LinkifyHeadersForTag(tagName) {
  var headers = document.getElementsByTagName(tagName);
  var header;
  for (var j = 0; j != headers.length; j++) {
    header = headers[j];
    if (!hasClass(header, 'ignoreLink') && ('id' in header)) {
      if (header.id != '') {
        LinkifyHeader(header, 'link.png', 21);
        header.style.left = '-46px';
        header.style.position = 'relative';
      }
    }
  }
}

// Linkify all h2, h3, and h4s. h1s are titles.
function LinkifyHeaders() {
  LinkifyHeadersForTag('h2');
  LinkifyHeadersForTag('h3');
  LinkifyHeadersForTag('h4');
}

/*
 * Initialize the style guide by showing all internal
 * elements and then linkifying the headers.
 */

function initStyleGuide() {
  LinkifyHeaders();
  CreateTOC('tocDiv');
}
