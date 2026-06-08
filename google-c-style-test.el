;;; google-c-style-test.el --- unit tests for google-c-style.el  -*- lexical-binding: t; -*-

;; Copyright 2022 Google LLC
;;
;; Licensed under the Apache License, Version 2.0 (the "License");
;; you may not use this file except in compliance with the License.
;; You may obtain a copy of the License at
;;
;;     https://www.apache.org/licenses/LICENSE-2.0
;;
;; Unless required by applicable law or agreed to in writing, software
;; distributed under the License is distributed on an "AS IS" BASIS,
;; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
;; See the License for the specific language governing permissions and
;; limitations under the License.

;;; Commentary:

;; Unit tests for ‘google-c-style.el’.

;;; Code:

(require 'google-c-style)

(require 'cc-mode)
(require 'ert)
(require 'ert-x)

(ert-deftest google-c-style-test/indent ()
  "Check that a golden file remains unchanged."
  (ert-with-test-buffer (:name "golden")
    (insert-file-contents (ert-resource-file "golden.cc"))
    (c++-mode)
    (google-set-c-style)
    (should (equal (buffer-string) (ert-buffer-string-reindented)))))

;;; google-c-style-test.el ends here
