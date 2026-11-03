/**
 * @license
 * Copyright Google Inc.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Various helper functions.
 */

/** @const {!Set<string>} */
const knownCallouts = new Set(['important', 'note', 'tip', 'warning']);

/**
 * Returns the callout type if the element starts with a known callout prefix.
 * @param {!Element} ele
 * @return {?string}
 */
function matchCallout(ele) {
  const match = /^\s*([a-z]+):/i.exec(ele.textContent);
  if (!match) {
    return null;
  }
  const callout = match[1].toLowerCase();
  return knownCallouts.has(callout) ? callout : null;
}

/**
 * If a paragraph starts with (e.g.) "Note:" or "Tip:" then add that
 * "callout class" to its element.
 * @param {!Document} document
 */
export function styleAlerts(document) {
  const selectors = [
    // Autodetect paragraphs that *look* like alerts to automatically convert to
    // a callout (put it into a blockquote). This is what internal g3mark does.
    '.markdown-body > p',
    // Process blockquotes that are extremely likely to be an "alert".
    '.markdown-body > blockquote > p:first-child',
  ];
  for (const ele of document.querySelectorAll(selectors.join(', '))) {
    const callout = matchCallout(ele);
    if (!callout) {
      continue;
    }

    // Convert plain paragraph to a blockquote before styling it further.
    let container = ele.parentElement;
    if (container.tagName !== 'BLOCKQUOTE') {
      container = document.createElement('blockquote');
      ele.replaceWith(container);
      container.appendChild(ele);
    }

    // Add the callout style to blockquotes.
    container.classList.add(`callout-${callout}`);
  }
}

/**
 * If a TOC exists, clean it up a bit to not take so much space.
 * @param {!Document} document
 */
export function tidyToc(document) {
  const toc = document.getElementById('markdown-toc');
  if (!toc) {
    return;
  }

  const zippy = document.createElement('details');
  const summary = document.createElement('summary');
  summary.textContent = 'Table of Contents';
  zippy.appendChild(summary);
  toc.replaceWith(zippy);
  zippy.appendChild(toc);
}
