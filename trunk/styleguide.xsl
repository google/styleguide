<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:dcq="http://purl.org/dc/qualifiers/1.0/"
xmlns:fo="http://www.w3.org/1999/XSL/Format">
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
              <LINK HREF="http://www.google.com/favicon.ico" type="image/x-icon"
                    rel="shortcut icon"/>
              <LINK HREF="styleguide.css"
                    type="text/css" rel="stylesheet"/>

              <SCRIPT language="javascript" type="text/javascript">

                function ShowHideByName(bodyName, buttonName) {
                  var bodyElements = document.getElementsByName(bodyName);
                  if (bodyElements.length != 1) {
                    alert("ShowHideByName() got the wrong number of bodyElements:  " + bodyElements.length);
                  } else {
                    var bodyElement = bodyElements[0];
                    var buttonElements = document.getElementsByName(buttonName);
                    var buttonElement = buttonElements[0];
                    if (bodyElement.style.display == "none" || bodyElement.style.display == "") {
                      bodyElement.style.display = "inline";
                      buttonElement.innerHTML = '<xsl:value-of select="$hide_button_text"/>';
                    } else {
                      bodyElement.style.display = "none";
                      buttonElement.innerHTML = '<xsl:value-of select="$show_button_text"/>';
                    }
                  }
                }

                function ShowHideAll() {
                  var allButtons = document.getElementsByName("show_hide_all_button");
                  var allButton = allButtons[0];
                  if (allButton.innerHTML == '<xsl:value-of select="$hide_button_text"/>') {
                    allButton.innerHTML = '<xsl:value-of select="$show_button_text"/>';
                    SetHiddenState(document.body.childNodes, "none", '<xsl:value-of select="$show_button_text"/>');
                  } else {
                    allButton.innerHTML = '<xsl:value-of select="$hide_button_text"/>';
                    SetHiddenState(document.body.childNodes, "inline", '<xsl:value-of select="$hide_button_text"/>');
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
                    if (root[i].className == 'stylepoint_body')  {
                      root[i].style.display = newState;
                    }
                  }
                }


                window.onload = function() {
                  // if the URL contains "?showall=y", expand the details of all children
                  {
                    var showHideAllRegex = new RegExp("[\\?&amp;](showall)=([^&amp;#]*)");
                    var showHideAllValue = showHideAllRegex.exec(window.location.href);
                    if (showHideAllValue != null) {
                      if (showHideAllValue[2] == "y") {
                        SetHiddenState(document.body.childNodes, "inline", '<xsl:value-of select="$hide_button_text"/>');
                      } else {
                        SetHiddenState(document.body.childNodes, "none", '<xsl:value-of select="$show_button_text"/>');
                      }
                    }
                    var showOneRegex = new RegExp("[\\?&amp;](showone)=([^&amp;#]*)");
                    var showOneValue = showOneRegex.exec(window.location.href);
                    if (showOneValue != null) {
                      var body_name = showOneValue[2] + '<xsl:value-of select="$body_suffix"/>';
                      var button_name = showOneValue[2] + '<xsl:value-of select="$button_suffix"/>';
                      ShowHideByName(body_name, button_name);
                    }

                  }
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
        <SPAN class="showhide_button" style="margin-left: 0;"><xsl:value-of select="$show_button_text"/></SPAN>.
        You may toggle all summaries with the big arrow button:
      </P>
      <DIV style=" font-size: larger; margin-left: +2em;">
        <SPAN class="showhide_button" style="font-size: 180%;">
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
    <H2>Overview</H2>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="PARTING_WORDS">
    <H2>Parting Words</H2>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="CATEGORY">
    <SPAN>
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
    </SPAN>
  </xsl:template>

  <xsl:template match="STYLEPOINT">
    <SPAN>
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
        <xsl:value-of select="$stylepoint_name"/><xsl:value-of select="$body_suffix"/>
        <xsl:text>','</xsl:text>
        <xsl:value-of select="$buttonName"/>
        <xsl:text>')</xsl:text>
      </xsl:variable>
      <SPAN class="showhide_button">
        <xsl:attribute name="onclick"><xsl:value-of select="$onclick_definition"/></xsl:attribute>
        <xsl:attribute name="name"><xsl:value-of select="$buttonName"/></xsl:attribute>
        <xsl:attribute name="id"><xsl:value-of select="$buttonName"/></xsl:attribute>
        <xsl:value-of select="$button_text"/>
      </SPAN>
      <xsl:apply-templates>
        <xsl:with-param name="anchor_prefix" select="$stylepoint_name" />
      </xsl:apply-templates>
    </SPAN>
  </xsl:template>

  <xsl:template match="SUMMARY">
    <xsl:param name="anchor_prefix" />
    <SPAN>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <xsl:apply-templates/>
    </SPAN>
  </xsl:template>

  <xsl:template match="BODY">
    <xsl:param name="anchor_prefix" />
    <SPAN>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <BR/>
      <SPAN class="stylepoint_body">
        <xsl:attribute name="name"><xsl:value-of select="$anchor_prefix"/><xsl:value-of select="$body_suffix"/></xsl:attribute>
        <xsl:attribute name="id"><xsl:value-of select="$anchor_prefix"/><xsl:value-of select="$body_suffix"/></xsl:attribute>
        <xsl:attribute name="style">
          <xsl:choose>
            <xsl:when test="$show_explanation_default">display: inline</xsl:when>
            <xsl:otherwise>display: none</xsl:otherwise>
          </xsl:choose>
        </xsl:attribute>
        <SPAN class="link_button">
          <A>
            <xsl:attribute name="href">?showone=<xsl:value-of select="$anchor_prefix"/>#<xsl:value-of select="$anchor_prefix"/></xsl:attribute>
            link
          </A>
        </SPAN>
        <xsl:apply-templates/>
      </SPAN>
    </SPAN>
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
      <SPAN style="font-size: 150%;">TODO:
        <xsl:apply-templates/>
      </SPAN>
    </P>
  </xsl:template>

  <xsl:template match="SUBSECTION">
    <P>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <SPAN class="stylepoint_subsection"><xsl:value-of select="@title"/>  </SPAN>
      <xsl:apply-templates/>
    </P>
  </xsl:template>

  <xsl:template match="CODE_SNIPPET">
    <SPAN>
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
    </SPAN>
  </xsl:template>

  <xsl:template match="BAD_CODE_SNIPPET">
    <SPAN>
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
    </SPAN>
  </xsl:template>

  <xsl:template match="SYNTAX">
    <I>
      <xsl:attribute name="class"><xsl:value-of select="@class"/></xsl:attribute>
      <xsl:apply-templates/>
    </I>
  </xsl:template>

  <!-- This passes through any HTML elements that the
    XML doc uses for minor formatting -->
  <xsl:template match="a|address|blockquote|br|center|cite|code|dd|div|dl|dt|em|hr|i|li|ol|p|pre|span|table|td|th|tr|ul|var|A|ADDRESS|BLOCKQUOTE|BR|CENTER|CITE|CODE|DD|DIV|DL|DT|EM|HR|I|LI|OL|P|PRE|SPAN|TABLE|TD|TH|TR|UL|VAR">
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
    <xsl:value-of select="translate($sectionname,' ()#','____')"/>
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
    <xsl:choose>
      <!-- $line (or $rest) is considered empty if we'd trim the entire line -->
      <xsl:when test="($strip = '1') and ($is_firstline = '1') and
                      (string-length($line) &lt;= $trim_count)">
      </xsl:when>
      <xsl:when test="($strip = '1') and
                      (string-length($rest) &lt;= $trim_count)">
        <xsl:value-of select="substring($line, $trim_count+1)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="substring($line, $trim_count+1)"/>
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

</xsl:stylesheet>

