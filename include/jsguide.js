// Defining a style guide initialization function
window.initStyleGuide = function(init) {
  // Utility function to iterate over elements matching a query selector
  function find(querySelector, callback) {
      // Using forEach directly on NodeList using Array.prototype.forEach.call
      Array.prototype.forEach.call(document.querySelectorAll(querySelector), callback);
  }
  
  // Adding the tocDiv below the title
  const title = document.querySelector('h1'); // Using querySelector for simplicity
  const toc = document.createElement('div');
  toc.id = 'tocDiv';
  toc.className = 'vertical_toc';
  title.parentNode.insertBefore(toc, title.nextSibling);
  
  // Adding "callout class" to paragraph elements starting with "Note:" or "Tip:"
  find('p', function(paragraph) {
      const match = /^([a-z]+):/i.exec(paragraph.textContent);
      if (match) paragraph.classList.add(match[1].toLowerCase());
  });
  
  // Filling in text for intra-document links
  find('a[href^="#"]', function(link) {
      const heading = document.getElementById(link.getAttribute('href').substring(1));
      if (heading && link.textContent == '??') link.textContent = heading.textContent;
  });
  
  // Adjusting code blocks for compatibility with prettify
  find('pre > code', function(code) {
      const pre = code.parentElement;
      if (['language-css', 'language-django', 'language-html', 'language-ts'].includes(code.className)) {
          code.classList.add('prettyprint');
      }
      pre.className = code.className;
      pre.innerHTML = code.innerHTML;
  });
  
  // Running the normal init function
  init();
  
  // Appending the pretty-print script to the document body
  const pretty = document.createElement('script');
  pretty.src = 'https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js';
  document.body.appendChild(pretty);
}.bind(null, window.initStyleGuide);
