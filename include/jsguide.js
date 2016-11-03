window.initStyleGuide = function(init) {
  // Runs the callback on every element matched by the query selector.
  function find(querySelector, callback) {
    var elements = [].slice.call(document.querySelectorAll(querySelector));
    for (var i = 0; i < elements.length; i++) {
      callback(elements[i]);
    }
  }
  // Add the tocDiv at the top.
  var title = document.getElementsByTagName('h1')[0];
  var toc = document.createElement('div');
  toc.id = 'tocDiv';
  toc.className = 'vertical_toc';
  title.parentNode.insertBefore(toc, title.nextSibling);

  // If a paragraph starts with (e.g.) "Note:" or "Tip:" then add
  // that "callout class" to its element.
  find('p', function(paragraph) {
    var match = /^([a-z]+):/i.exec(paragraph.textContent);
    if (match) {
      paragraph.classList.add(match[1].toLowerCase());
    }
  });

  // Fill in text for intra-document links, ensuring that links
  // remain up-to-date even if sections are moved or renumbered.
  // This triggers on any link with "??" as its text and a URL
  // starting with "#", and the filled-in text is exactly the same
  // as the text of the referenced section heading.
  find('a[href^="#"]', function(link) {
    var href = link.getAttribute('href');
    var heading = document.getElementById(href.substring(1));
    // Fill in link text with heading title
    if (heading && link.textContent == '??') {
      link.textContent = heading.textContent;
    }
  });

  // Hoedown renders fenced code blocks incompatibly with what
  // prettify expects. As a result, prettify doesn't handle them
  // properly. Fix it by moving the code directly into the pre.
  find('pre > code', function(code) {
    var pre = code.parentElement;
    pre.className = code.className;
    pre.innerHTML = code.innerHTML;
  });

  // Run the normal init function.
  init();

  // Call the pretty-printer after we've fixed up the code blocks.
  var pretty = document.createElement('script');
  pretty.src = 'https://cdn.rawgit.com/google/code-prettify/master/loader/' +
      'run_prettify.js';
  document.body.appendChild(pretty);
}.bind(null, window.initStyleGuide);
