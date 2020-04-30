<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:dcq="http://purl.org/dc/qualifiers/1.0/"
xmlns:fo="http://www.w3.org/1999/XSL/Format"
xmlns:fn="http://www.w3.org/2005/xpath-functions">
  <xsl:output method="html"/>
  <!-- Set to 1 to show explanations by default.  Set to 0 to hide them -->
  <xsl:variable name="show_explanation_default" select="0" />
  <!-- The characters within the Webdings font that show the triangles -->
  <xsl:variable name="show_button_text" select="'&#x25B6;'" />
  <xsl:variable name="hide_button_text" select="'&#x25BD;'" />
  <!-- The suffix for names -->
  <xsl:variable name="button_suffix" select="'__button'"/>
  <xsl:variable name="body_suffix" select="'__body'"/>
  <!-- For easy reference, the name of the button -->
  <xsl:variable name="show_hide_all_button" select="'show_hide_all_button'"/>

  <!-- The top-level element -->
  <xsl:template match="GUIDE">
      <HTML>
          <HEAD>
              <TITLE><xsl:value-of select="@title"/></TITLE>
              <META http-equiv="Content-Type" content="text/html; charset=utf-8"/>
              <META http-equiv="refresh" content="0;url=https://google.github.io/styleguide/shellguide.html" />
              <LINK rel="canonical" href="https://google.github.io/styleguide/shellguide.html" />
              <LINK HREF="https://www.google.com/favicon.ico" type="image/x-icon"
                    rel="shortcut icon"/>
              <LINK HREF="styleguide.css"
                    type="text/css" rel="stylesheet"/>

              <SCRIPT language="javascript" type="text/javascript">

                function GetElementsByName(name) {
                  // Workaround a bug on old versions of opera.
                  if (document.getElementsByName) {
                    return document.getElementsByName(name);
                  } else {
                    return [document.getElementById(name)];
                  }
                }

                /**
                 * @param {string} namePrefix The prefix of the body name.
                 * @param {function(boolean): boolean} getVisibility Computes the new
                 *     visibility state, given the current one.
                 */
                function ChangeVisibility(namePrefix, getVisibility) {
                  var bodyName = namePrefix + '<xsl:value-of select="$body_suffix"/>';
                  var buttonName = namePrefix + '<xsl:value-of select="$button_suffix"/>';
                  var bodyElements = GetElementsByName(bodyName);
                  var linkElement = GetElementsByName('link-' + buttonName)[0];
                  if (bodyElements.length != 1) {
                    throw Error('ShowHideByName() got the wrong number of bodyElements:  ' + 
                        bodyElements.length);
                  } else {
                    var bodyElement = bodyElements[0];
                    var buttonElement = GetElementsByName(buttonName)[0];
                    var isVisible = bodyElement.style.display != "none";
                    if (getVisibility(isVisible)) {
                      bodyElement.style.display = "inline";
                      linkElement.style.display = "block";
                      buttonElement.innerHTML = '<xsl:value-of select="$hide_button_text"/>';
                    } else {
                      bodyElement.style.display = "none";
                      linkElement.style.display = "none";
                      buttonElement.innerHTML = '<xsl:value-of select="$show_button_text"/>';
                    }
                  }
                }

                function ShowHideByName(namePrefix) {
                  ChangeVisibility(namePrefix, function(old) { return !old; });
                }

                function ShowByName(namePrefix) {
                  ChangeVisibility(namePrefix, function() { return true; });
                }

                function ShowHideAll() {
                  var allButton = GetElementsByName("show_hide_all_button")[0];
                  if (allButton.innerHTML == '<xsl:value-of select="$hide_button_text"/>') {
                    allButton.innerHTML = '<xsl:value-of select="$show_button_text"/>';
                    SetHiddenState(document.getElementsByTagName("body")[0].childNodes, "none", '<xsl:value-of select="$show_button_text"/>');
                  } else {
                    allButton.innerHTML = '<xsl:value-of select="$hide_button_text"/>';
                    SetHiddenState(document.getElementsByTagName("body")[0].childNodes, "inline", '<xsl:value-of select="$hide_button_text"/>');
                  }
                }

                // Recursively sets state of all children
                // of a particular node.
                function SetHiddenState(root, newState, newButton) {
                  for (var i = 0; i != root.length; i++) {
                    SetHiddenState(root[i].childNodes, newState, newButton);
                    if (root[i].className == 'showhide_button')  {
                      root[i].innerHTML = newButton;
                    }
                    if (root[i].className == 'stylepoint_body' ||
                        root[i].className == 'link_button')  {
                      root[i].style.display = newState;
                    }
                  }
                }


                function EndsWith(str, suffix) {
                  var l = str.length - suffix.length;
                  return l >= 0 &amp;&amp; str.indexOf(suffix, l) == l;
                }

                function RefreshVisibilityFromHashParam() {
                  var hashRegexp = new RegExp('#([^&amp;#]*)$');
                  var hashMatch = hashRegexp.exec(window.location.href);
                  var anchor = hashMatch &amp;&amp; GetElementsByName(hashMatch[1])[0];
                  var node = anchor;
                  var suffix = '<xsl:value-of select="$body_suffix"/>';
                  while (node) {
                    var id = node.id;
                    var matched = id &amp;&amp; EndsWith(id, suffix);
                    if (matched) {
                      var len = id.length - suffix.length;
                      ShowByName(id.substring(0, len));
                      if (anchor.scrollIntoView) {
                        anchor.scrollIntoView();
                      }

                      return;
                    }
                    node = node.parentNode;
                  }
                }

                window.onhashchange = RefreshVisibilityFromHashParam;

                window.onload = function() {
                  // if the URL contains "?showall=y", expand the details of all children
                  var showHideAllRegex = new RegExp("[\\?&amp;](showall)=([^&amp;#]*)");
                  var showHideAllValue = showHideAllRegex.exec(window.location.href);
                  if (showHideAllValue != null) {
                    if (showHideAllValue[2] == "y") {
                      SetHiddenState(document.getElementsByTagName("body")[0].childNodes, 
                          "inline", '<xsl:value-of select="$hide_button_text"/>');
                    } else {
                      SetHiddenState(document.getElementsByTagName("body")[0].childNodes, 
                          "none", '<xsl:value-of select="$show_button_text"/>');
                    }
                  }
                  var showOneRegex = new RegExp("[\\?&amp;](showone)=([^&amp;#]*)");
                  var showOneValue = showOneRegex.exec(window.location.href);
                  if (showOneValue) {
                    ShowHideByName(showOneValue[2]);
                  }


                  RefreshVisibilityFromHashParam();
                }
              </SCRIPT>
          </HEAD>
          <BODY>
            <H1><xsl:value-of select="@title"/></H1>
              <xsl:apply-templates/>
          </BODY>
      </HTML>
  </xsl:template>

  <!-- This passes through any HTML elements that the
    XML doc uses for minor formatting -->
  <xsl:template match="a|address|blockquote|br|center|cite|code|dd|div|dl|dt|em|hr|i|img|li|ol|p|pre|span|table|td|th|tr|ul|var|A|ADDRESS|BLOCKQUOTE|BR|CENTER|CITE|CODE|DD|DIV|DL|DT|EM|HR|I|LI|OL|P|PRE|SPAN|TABLE|TD|TH|TR|UL|VAR">
      <xsl:element name="{local-name()}">
          <xsl:copy-of select="@*"/>
          <xsl:apply-templates/>
      </xsl:element>
  </xsl:template>

</xsl:stylesheet>

