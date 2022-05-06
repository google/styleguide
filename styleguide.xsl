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

  <xsl:template match="OVERVIEW">
    <xsl:variable name="button_text">
      <xsl:choose>
        <xsl:when test="$show_explanation_default">
          <xsl:value-of select="$hide_button_text"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$show_button_text"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <DIV style="margin-left: 50%; font-size: 75%;">
      <P>
        Each style point has a summary for which additional information is available
        by toggling the accompanying arrow button that looks this way:
        <SPAN class="showhide_button" style="margin-left: 0; float: none">
          <xsl:value-of select="$show_button_text"/></SPAN>.
        You may toggle all summaries with the big arrow button:
      </P>
      <DIV style=" font-size: larger; margin-left: +2em;">
        <SPAN class="showhide_button" style="font-size: 180%; float: none">
          <xsl:attribute name="onclick"><xsl:value-of select="'javascript:ShowHideAll()'"/></xsl:attribute>
          <xsl:attribute name="name"><xsl:value-of select="$show_hide_all_button"/></xsl:attribute>
          <xsl:attribute name="id"><xsl:value-of select="$show_hide_all_button"/></xsl:attribute>
          <xsl:value-of select="$button_text"/>
        </SPAN>
        Toggle all summaries
      </DIV>
    </DIV>
    <xsl:call-template name="TOC">
      <xsl:with-param name="root" select=".."/>
    </xsl:call-template>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="PARTING_WORDS">
    <H2>Parting Words</H2>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="CATEGORY">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <H2>
        <xsl:variable name="category_name">
          <xsl:call-template name="anchorname">
            <xsl:with-param name="sectionname" select="@title"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:attribute name="name"><xsl:value-of select="$category_name"/></xsl:attribute>
        <xsl:attribute name="id"><xsl:value-of select="$category_name"/></xsl:attribute>
        <xsl:value-of select="@title"/>
      </H2>
      <xsl:apply-templates/>
    </DIV>
  </xsl:template>

  <xsl:template match="STYLEPOINT">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <xsl:variable name="stylepoint_name">
        <xsl:call-template name="anchorname">
          <xsl:with-param name="sectionname" select="@title"/>
        </xsl:call-template>
      </xsl:variable>
      <xsl:variable name="button_text">
        <xsl:choose>
          <xsl:when test="$show_explanation_default">
            <xsl:value-of select="$hide_button_text"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="$show_button_text"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <H3>
        <A>
          <xsl:attribute name="name"><xsl:value-of select="$stylepoint_name"/></xsl:attribute>
          <xsl:attribute name="id"><xsl:value-of select="$stylepoint_name"/></xsl:attribute>
          <xsl:value-of select="@title"/>
        </A>
      </H3>
      <xsl:variable name="buttonName">
        <xsl:value-of select="$stylepoint_name"/><xsl:value-of select="$button_suffix"/>
      </xsl:variable>
      <xsl:variable name="onclick_definition">
        <xsl:text>javascript:ShowHideByName('</xsl:text>
        <xsl:value-of select="$stylepoint_name"/>
        <xsl:text>')</xsl:text>
      </xsl:variable>
      <SPAN class="link_button" id="link-{$buttonName}" name="link-{$buttonName}">
        <A>
          <xsl:attribute name="href">?showone=<xsl:value-of select="$stylepoint_name"/>#<xsl:value-of select="$stylepoint_name"/></xsl:attribute>
          link
        </A>
      </SPAN>
      <SPAN class="showhide_button">
        <xsl:attribute name="onclick"><xsl:value-of select="$onclick_definition"/></xsl:attribute>
        <xsl:attribute name="name"><xsl:value-of select="$buttonName"/></xsl:attribute>
        <xsl:attribute name="id"><xsl:value-of select="$buttonName"/></xsl:attribute>
        <xsl:value-of select="$button_text"/>
      </SPAN>
      <xsl:apply-templates>
        <xsl:with-param name="anchor_prefix" select="$stylepoint_name" />
      </xsl:apply-templates>
    </DIV>
  </xsl:template>

  <xsl:template match="SUMMARY">
    <xsl:param name="anchor_prefix" />
    <DIV style="display:inline;">
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <xsl:apply-templates/>
    </DIV>
  </xsl:template>

  <xsl:template match="BODY">
    <xsl:param name="anchor_prefix" />
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <DIV class="stylepoint_body">
        <xsl:attribute name="name"><xsl:value-of select="$anchor_prefix"/><xsl:value-of select="$body_suffix"/></xsl:attribute>
        <xsl:attribute name="id"><xsl:value-of select="$anchor_prefix"/><xsl:value-of select="$body_suffix"/></xsl:attribute>
        <xsl:attribute name="style">
          <xsl:choose>
            <xsl:when test="$show_explanation_default">display: inline</xsl:when>
            <xsl:otherwise>display: none</xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
        <xsl:apply-templates/>
      </DIV>
    </DIV>
  </xsl:template>

  <xsl:template match="DEFINITION">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_section">Definition:  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="PROS">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_section">Pros:  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="CONS">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_section">Cons: </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="DECISION">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_section">Decision:  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="TODO">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <DIV style="font-size: 150%;">TODO:
        <xsl:apply-templates/>
      </DIV>
    </P>
  </xsl:template>

  <xsl:template match="SUBSECTION">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_subsection"><xsl:value-of select="@title"/>  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="SUBSUBSECTION">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_subsubsection"><xsl:value-of select="@title"/>  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="CODE_SNIPPET">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <PRE><xsl:call-template name="print_without_leading_chars">
           <xsl:with-param name="text" select="."/>
           <xsl:with-param name="strip" select="1"/>
           <xsl:with-param name="is_firstline" select="1"/>
           <xsl:with-param name="trim_count">
             <xsl:call-template name="num_leading_spaces">
               <xsl:with-param name="text" select="."/>
               <xsl:with-param name="max_so_far" select="1000"/>
             </xsl:call-template>
           </xsl:with-param>
         </xsl:call-template></PRE>
    </DIV>
  </xsl:template>

  <xsl:template match="BAD_CODE_SNIPPET">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <PRE class="badcode"><xsl:call-template name="print_without_leading_chars">
           <xsl:with-param name="text" select="."/>
           <xsl:with-param name="strip" select="1"/>
           <xsl:with-param name="is_firstline" select="1"/>
           <xsl:with-param name="trim_count">
             <xsl:call-template name="num_leading_spaces">
               <xsl:with-param name="text" select="."/>
               <xsl:with-param name="max_so_far" select="1000"/>
             </xsl:call-template>
           </xsl:with-param>
         </xsl:call-template></PRE>
    </DIV>
  </xsl:template>

  <xsl:template match="PY_CODE_SNIPPET">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <PRE><xsl:call-template name="print_python_code">
             <xsl:with-param name="text" select="."/>
           </xsl:call-template></PRE>
    </DIV>
  </xsl:template>

  <xsl:template match="BAD_PY_CODE_SNIPPET">
    <DIV>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <PRE class="badcode"><xsl:call-template name="print_python_code">
                             <xsl:with-param name="text" select="."/>
                           </xsl:call-template></PRE>
    </DIV>
  </xsl:template>

  <xsl:template match="FUNCTION">
    <xsl:call-template name="print_function_name">
      <xsl:with-param name="text" select="."/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="SYNTAX">
    <I>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <xsl:apply-templates/>
    </I>
  </xsl:template>


  <!-- This passes through any HTML elements that the
    XML doc uses for minor formatting -->
  <xsl:template match="a|address|blockquote|br|center|cite|code|dd|div|dl|dt|em|hr|i|img|li|ol|p|pre|span|table|td|th|tr|ul|var|A|ADDRESS|BLOCKQUOTE|BR|CENTER|CITE|CODE|DD|DIV|DL|DT|EM|HR|I|LI|OL|P|PRE|SPAN|TABLE|TD|TH|TR|UL|VAR">
      <xsl:element name="{local-name()}">
          <xsl:copy-of select="@*"/>
          <xsl:apply-templates/>
      </xsl:element>
  </xsl:template>

    <!-- Builds the table of contents -->
  <xsl:template name="TOC">
    <xsl:param name="root"/>
    <DIV class="toc">
      <DIV class="toc_title">Table of Contents</DIV>
      <TABLE>
      <xsl:for-each select="$root/CATEGORY">
        <TR valign="top">
          <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
          <TD>
          <DIV class="toc_category">
            <A>
              <xsl:attribute name="href">
                <xsl:text>#</xsl:text>
                <xsl:call-template name="anchorname">
                  <xsl:with-param name="sectionname" select="@title"/>
                </xsl:call-template>
              </xsl:attribute>
              <xsl:value-of select="@title"/>
            </A>
          </DIV>
          </TD><TD>
            <DIV class="toc_stylepoint">
              <xsl:for-each select="./STYLEPOINT">
                <SPAN style="padding-right: 1em; white-space:nowrap;">
                  <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
                  <A>
                    <xsl:attribute name="href">
                      <xsl:text>#</xsl:text>
                      <xsl:call-template name="anchorname">
                        <xsl:with-param name="sectionname" select="@title"/>
                      </xsl:call-template>
                    </xsl:attribute>
                    <xsl:value-of select="@title"/>
                  </A>
                </SPAN>
                <xsl:text> </xsl:text>
              </xsl:for-each>
            </DIV>
          </TD>
        </TR>
      </xsl:for-each>
      </TABLE>
    </DIV>
  </xsl:template>

  <xsl:template name="TOC_one_stylepoint">
    <xsl:param name="stylepoint"/>
  </xsl:template>

  <!-- Creates a standard anchor given any text.
       Substitutes underscore for characters unsuitable for URLs  -->
  <xsl:template name="anchorname">
    <xsl:param name="sectionname"/>
    <!-- strange quoting necessary to strip apostrophes -->
    <xsl:variable name="bad_characters" select="&quot; ()#'&quot;"/>
    <xsl:value-of select="translate($sectionname,$bad_characters,'_____')"/>
  </xsl:template>

  <!-- Given text, evaluates to the number of leading spaces. -->
  <!-- TODO(csilvers): deal well with leading tabs (treat as 8 spaces?) -->
  <xsl:template name="num_leading_spaces_one_line">
    <xsl:param name="text"/>
    <xsl:param name="current_count"/>
    <xsl:choose>
      <xsl:when test="starts-with($text, ' ')">
        <xsl:call-template name="num_leading_spaces_one_line">
          <xsl:with-param name="text" select="substring($text, 2)"/>
          <xsl:with-param name="current_count" select="$current_count + 1"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$current_count"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Given a block of text, each line terminated by \n, evaluates to
       the indentation-level of that text; that is, the largest number
       n such that every non-blank line starts with at least n spaces. -->
  <xsl:template name="num_leading_spaces">
    <xsl:param name="text"/>
    <xsl:param name="max_so_far"/>
    <!-- TODO(csilvers): deal with case text doesn't end in a newline -->
    <xsl:variable name="line" select="substring-before($text, '&#xA;')"/>
    <xsl:variable name="rest" select="substring-after($text, '&#xA;')"/>
    <xsl:variable name="num_spaces_this_line">
      <xsl:choose>
        <xsl:when test="$line=''">
           <xsl:value-of select="$max_so_far"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="num_leading_spaces_one_line">
            <xsl:with-param name="text" select="$line"/>
            <xsl:with-param name="current_count" select="0"/>
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:variable name="new_max_so_far">
       <xsl:choose>
         <xsl:when test="$num_spaces_this_line &lt; $max_so_far">
           <xsl:value-of select="$num_spaces_this_line"/>
         </xsl:when>
         <xsl:otherwise>
           <xsl:value-of select="$max_so_far"/>
         </xsl:otherwise>
       </xsl:choose>
    </xsl:variable>
    <!-- now check if we're on the last line, and if not, recurse -->
    <xsl:if test="$rest=''">
      <xsl:value-of select="$new_max_so_far"/>
    </xsl:if>
    <xsl:if test="not($rest='')">
      <xsl:call-template name="num_leading_spaces">
        <xsl:with-param name="text" select="$rest"/>
        <xsl:with-param name="max_so_far" select="$new_max_so_far"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- Given text, determine the starting position of code.
       This similar to num_leading_spaces_one_line but treats "Yes:" and "No:" 
       as spaces. Also, if there is no code on the first line, it searches 
       subsequent lines until a non-empty line is found.
       Used to find the start of code in snippets like:
       Yes: if(foo):
       No : if(foo):
       As well as:
       Yes:
         if (foo):
  -->
  <xsl:template name="code_start_index">
    <xsl:param name="text"/>
    <xsl:param name="current_count"/>
    <xsl:choose>
      <xsl:when test="starts-with($text, ' ')">
        <xsl:call-template name="code_start_index">
          <xsl:with-param name="text" select="substring($text, 2)"/>
          <xsl:with-param name="current_count" select="$current_count + 1"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="starts-with($text, 'Yes:')">
        <xsl:call-template name="code_start_index">
          <xsl:with-param name="text" select="substring($text, 5)"/>
          <xsl:with-param name="current_count" select="$current_count + 4"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="starts-with($text, 'No:')">
        <xsl:call-template name="code_start_index">
          <xsl:with-param name="text" select="substring($text, 4)"/>
          <xsl:with-param name="current_count" select="$current_count + 3"/>
        </xsl:call-template>
      </xsl:when>
      <!-- This is only reached if the first line is entirely whitespace or 
           contains nothing but "Yes:" or "No:"-->
      <xsl:when test="starts-with($text, '&#xA;')">
        <xsl:call-template name="code_start_index">
          <xsl:with-param name="text" select="substring($text, 2)"/>
          <xsl:with-param name="current_count" select="0"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$current_count"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Helper for ends_with_colon. Determine whether the given line is nothing
       but spaces and python-style comments. -->
  <xsl:template name="is_blank_or_comment">
    <xsl:param name="line"/>
    <xsl:choose>
      <xsl:when test="$line = ''">
        <xsl:value-of select="1"/>
      </xsl:when>
      <xsl:when test="starts-with($line, '&#xA;')">
        <xsl:value-of select="1"/>
      </xsl:when>
      <xsl:when test="starts-with($line, '#')">
        <xsl:value-of select="1"/>
      </xsl:when>
      <xsl:when test="starts-with($line, ' ')">
        <xsl:call-template name="is_blank_or_comment">
          <xsl:with-param name="line" select="substring($line, 2)"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="0"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Determine whether the given line ends with a colon. Note that Python
       style comments are ignored so the following lines return True:
       - def foo():
       - def foo():  # Bar
       - if(foo):

       But some code may confuse this function. For example the following are
       also consider to "end_with_colon" even though they don't for Python
       - foo(":  #")
       - foo() # No need for :
  -->
  <xsl:template name="ends_with_colon">
    <xsl:param name="line"/>
    <xsl:param name="found_colon"/>
    <xsl:choose>
      <xsl:when test="$line = ''">
        <xsl:value-of select="$found_colon"/>
      </xsl:when>
      <xsl:when test="starts-with($line, '&#xA;')">
        <xsl:value-of select="$found_colon"/>
      </xsl:when>
      <xsl:when test="starts-with($line, ' ')">
        <xsl:call-template name="ends_with_colon">
          <xsl:with-param name="line" select="substring($line, 2)"/>
          <xsl:with-param name="found_colon" select="$found_colon"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="starts-with($line, ':')">
        <xsl:variable name="rest_is_comment">
          <xsl:call-template name="is_blank_or_comment">
            <xsl:with-param name="line" select="substring($line, 2)"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:choose>
          <xsl:when test="$rest_is_comment = '1'">
            <xsl:value-of select="1"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="ends_with_colon">
              <xsl:with-param name="line" select="substring($line, 2)"/>
              <xsl:with-param name="found_colon" select="0"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="ends_with_colon">
          <xsl:with-param name="line" select="substring($line, 2)"/>
          <xsl:with-param name="found_colon" select="0"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Prints one line of python code with proper indent and calls itself
       recursively for the rest of the text.
       This template uses "a", "b", "c" and "d" to refer to four key column
       numbers. They are:
       - a: the indentation common to all lines in a code snippet. This is
            stripped out to allow for cleaner code in the xml.
       - b: the indentation of the most out-dented line of code. This is
            different from "a" when code is labelled with "Yes:" or "No:"
       - c: the indentation of the current python block, in other words, the
            indentation of the first line of this block, which is the
            indentation of the last line we saw that ended with a colon.
       - d: the "total" indentation of the line, ignoring possible "Yes:" or
            "No:" text on the line.

       For example, for the last line of the following code snippet, the
       positions of a, b, c and d are indicated below:
           Yes: def Foo():
                  if bar():
                    a += 1
                    baz()
           a    b c d

       The algorithm is:
       1) Split the text into first line and the rest. Note that the
          substring-before function is supposed to handle the case where the
          character is not present in the string but does not so we
          automatically ignore the last line of the snippet which is always
          empty (the closing snippet tag). This is consistent with the
          behavior or print_without_leading_chars.
       2) If the current is empty (only whitespace), print newline and call
          itself recursively on the rest of the text with the rest of the
          parameters unchanged.
       3) Otherwise, measure "d"
       4) Measure "c" by taking:
          - the value of "d" if the previous line ended with a colon or the
            current line is outdented compare to the previous line
          - the indent of the previous line otherwise
       5) Print line[a:c] (Note that we ignore line[0:a])
       6) Print line[b:c] in an external span (in order to double the block
          indent in external code).
       7) Print line[c:<end>] with function names processed to produce both 
          internal and external names.
       8) If there are more lines, recurse.
  -->
  <xsl:template name="print_python_line_recursively">
    <xsl:param name="text"/>
    <xsl:param name="a"/>
    <xsl:param name="b"/>
    <xsl:param name="previous_indent"/>
    <xsl:param name="previous_ends_with_colon"/>
    <xsl:param name="is_first_line"/>
    <xsl:variable name="line" select="substring-before($text, '&#xA;')"/>
    <xsl:variable name="rest" select="substring-after($text, '&#xA;')"/>
    <xsl:choose>
      <xsl:when test="substring($line, $b) = '' and not($rest = '')">
        <xsl:if test="not($is_first_line = '1')">
          <xsl:text>&#xA;</xsl:text>
        </xsl:if>
        <xsl:call-template name="print_python_line_recursively">
          <xsl:with-param name="text" select="$rest"/>
          <xsl:with-param name="a" select="$a"/>
          <xsl:with-param name="b" select="$b"/>
          <xsl:with-param name="previous_indent" select="$previous_indent"/>
          <xsl:with-param name="previous_ends_with_colon"
                          select="$previous_ends_with_colon"/>
          <xsl:with-param name="is_first_line" select="0"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="indent_after_b">
          <xsl:call-template name="num_leading_spaces_one_line">
            <xsl:with-param name="text" select="substring($line, $b + 1)"/>
            <xsl:with-param name="current_count" select="0"/>
          </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="d" select="$b + $indent_after_b"/>
        <xsl:variable name="c">
           <xsl:choose>
             <xsl:when test="$previous_ends_with_colon = '1' or
                             $previous_indent > $d">
               <xsl:value-of select="$d"/>
             </xsl:when>
             <xsl:otherwise>
               <xsl:value-of select="$previous_indent"/>
             </xsl:otherwise>
           </xsl:choose>
        </xsl:variable>

        <xsl:value-of select="substring($line, $a + 1, $c - $a)"/>
        <span class="external">
           <xsl:value-of select="substring($line, $b + 1, $c - $b)"/>
        </span>
        <xsl:call-template name="munge_function_names_in_text">
          <xsl:with-param name="stripped_line"
             select="substring($line, $c + 1)"/>
        </xsl:call-template>
        <xsl:if test="not(substring($rest, $a) = '')">
          <xsl:text>&#xA;</xsl:text>
          <xsl:call-template name="print_python_line_recursively">
            <xsl:with-param name="text" select="$rest"/>
            <xsl:with-param name="a" select="$a"/>
            <xsl:with-param name="b" select="$b"/>
            <xsl:with-param name="previous_indent" select="$c"/>
            <xsl:with-param name="previous_ends_with_colon">
              <xsl:call-template name="ends_with_colon">
                <xsl:with-param name="line" select="$line"/>
                <xsl:with-param name="found_colon" select="0"/>
              </xsl:call-template>
            </xsl:with-param>
            <xsl:with-param name="is_first_line" select="0"/>
          </xsl:call-template>
        </xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Print python code with internal and external styles.
       In order to conform with PEP-8 externally, we identify 2-space indents
       and an external-only 4-space indent.
       Function names that are marked with $$FunctionName/$$ have an external
       lower_with_underscore version added. -->
  <xsl:template name="print_python_code">
    <xsl:param name="text"/>

    <xsl:variable name="a">
       <xsl:call-template name="num_leading_spaces">
         <xsl:with-param name="text" select="."/>
         <xsl:with-param name="max_so_far" select="1000"/>
       </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="b">
      <xsl:call-template name="code_start_index">
        <xsl:with-param name="text" select="$text"/>
        <xsl:with-param name="current_count" select="0"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:call-template name="print_python_line_recursively">
      <xsl:with-param name="text" select="$text"/>
      <xsl:with-param name="a" select="$a"/>
      <xsl:with-param name="b" select="$b"/>
      <xsl:with-param name="previous_indent" select="$b"/>
      <xsl:with-param name="previous_ends_with_colon" select="0"/>
      <xsl:with-param name="is_first_line" select="1"/> 
    </xsl:call-template>
  </xsl:template>

  <!-- Given a block of text, each line terminated by \n, and a number n,
       emits the text with the first n characters of each line
       deleted.  If strip==1, then we omit blank lines at the beginning
       and end of the text (but not the middle!) -->
  <!-- TODO(csilvers): deal well with leading tabs (treat as 8 spaces?) -->
  <xsl:template name="print_without_leading_chars">
    <xsl:param name="text"/>
    <xsl:param name="trim_count"/>
    <xsl:param name="strip"/>
    <xsl:param name="is_firstline"/>
    <!-- TODO(csilvers): deal with case text doesn't end in a newline -->
    <xsl:variable name="line" select="substring-before($text, '&#xA;')"/>
    <xsl:variable name="rest" select="substring-after($text, '&#xA;')"/>
    <xsl:variable name="stripped_line" select="substring($line, $trim_count+1)"/>
    <xsl:choose>
      <!-- $line (or $rest) is considered empty if we'd trim the entire line -->
      <xsl:when test="($strip = '1') and ($is_firstline = '1') and
                      (string-length($line) &lt;= $trim_count)">
      </xsl:when>
      <xsl:when test="($strip = '1') and
                      (string-length($rest) &lt;= $trim_count)">
        <xsl:value-of select="$stripped_line"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$stripped_line"/>
        <xsl:text>&#xA;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="not($rest='')">
      <xsl:call-template name="print_without_leading_chars">
        <xsl:with-param name="text" select="$rest"/>
        <xsl:with-param name="trim_count" select="$trim_count"/>
        <xsl:with-param name="strip" select="$strip"/>
        <xsl:with-param name="is_firstline" select="0"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- Given a line of code, find function names that are marked with $$ /$$ and
       print out the line with the internal and external versions of the
       function names.-->
  <xsl:template name="munge_function_names_in_text">
    <xsl:param name="stripped_line"/>
    <xsl:choose>
      <xsl:when test="contains($stripped_line, '$$')">
        <xsl:value-of select="substring-before($stripped_line, '$$')"/>
        <xsl:call-template name="print_function_name">
          <xsl:with-param name="text" select="substring-after(substring-before($stripped_line, '/$$'), '$$')"/>
        </xsl:call-template>
        <xsl:call-template name="munge_function_names_in_text">
          <xsl:with-param name="stripped_line" select="substring-after($stripped_line, '/$$')"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$stripped_line"/>
     </xsl:otherwise>
   </xsl:choose>
  </xsl:template>

  <!-- Given a function name, print out both the internal and external version
       of the function name in their respective spans.-->
  <xsl:template name="print_function_name">
    <xsl:param name="text"/>
      <xsl:call-template name="convert_camel_case_to_lowercase_with_under">
        <xsl:with-param name="text" select="$text"/>
      </xsl:call-template>
  </xsl:template>

  <!-- Given a single word of text convert it from CamelCase to
       lower_with_under.
       This means replacing each uppercase character with _ followed by the
       lowercase version except for the first character which is replaced 
       without adding the _.-->
  <xsl:template name="convert_camel_case_to_lowercase_with_under">
    <xsl:param name="text"/>
    <xsl:param name="is_recursive_call"/>
    <xsl:variable name="first_char" select="substring($text, 1, 1)"/>
    <xsl:variable name="rest" select="substring($text, 2)"/>
    <xsl:choose>
      <xsl:when test="contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', $first_char)">
        <xsl:if test="$is_recursive_call='1'">
           <xsl:text>_</xsl:text>
        </xsl:if>
        <xsl:value-of select="translate($first_char, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$first_char" />
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="not($rest='')">
      <xsl:call-template name="convert_camel_case_to_lowercase_with_under">
        <xsl:with-param name="text" select="$rest"/>
        <xsl:with-param name="is_recursive_call" select="1"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>

