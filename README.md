구글 스타일 가이드
===================

모든 대형 오픈 소스 프로젝트는 고유의 스타일 가이드 - 프로젝트를 위한 코드 작성에 대한 관례의 모음(때로는 제멋대로이기도 한) - 를 가지고 있습니다. 코드가 일관된 스타일로 작성되면 거대한 코드베이스를 이해하는 것이 훨씬 쉬워집니다.

"변수명에는 낙타표기법을 사용할 것"에서 "전역 변수에는 절대 사용하지 말 것" 혹은 "예외(exception)을 절대 사용하지 말 것"까지, "스타일"은 많은 부분을 의미합니다. 이 프로젝트 
([google/styleguide](https://github.com/google/styleguide)) 링크는 
구글 코드에 사용하는 스타일 가이드라인입니다. 구글에서 비롯된 프로젝트를 
수정한다면 그 프로젝트에 적용하기 위한 스타일 가이드에 대한 페이지로 이곳에 
도달하셨을 지도 모릅니다.


이 프로젝트는 [C++ Style Guide][cpp], [Objective-C Style Guide][objc],
[Java Style Guide][java], [Python Style Guide][py], [R Style Guide][r],
[Shell Style Guide][sh], [HTML/CSS Style Guide][htmlcss],
[JavaScript Style Guide][js], [AngularJS Style Guide][angular],
[Common Lisp Style Guide][cl], 그리고 [Vimscript Style Guide][vim]를 가지고
 있습니다. 또한 이 프로젝트는 스타일 가이드 준수를 돕기 위한 도구인 [cpplint][cpplint]와, 구글 스타일을 위한 Emacs 설정 파일인 [google-c-style.el][emacs]를 
 포함하고 있습니다.

만약 여러분의 프로젝트에서 새로운 XML 문서 형식을 생성해야 한다면 [XML
Document Format Style Guide][xml]이 도움이 될 것입니다. 실제 스타일 규칙에 
더하여 서식을 직접 설계할 지, 기존의 형식을 적용할 지 여부와 XML 인스턴스 문서의 서식, 엘리먼트와 속성 중 어느 것을 사용할 지에 대한 조언들도 포함합니다.

이 문서들의 공유를 장려하기 위해, 프로젝트의 스타일 가이드는 CC-By 3.0 License를 따릅니다. 
자세한 내용은 [https://creativecommons.org/licenses/by/3.0/][ccl]를 참조하십시오.

다음은 이 프로젝트 외부의 구글 스타일 가이드입니다:
[Go Code Review Comments][go] and [Effective Dart][dart].

<a rel="license" href="https://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>

[cpp]: https://laterality.github.io/styleguide/cppguide.html
[objc]: objcguide.md
[java]: https://laterality.github.io/styleguide/javaguide.html
[py]: https://laterality.github.io/styleguide/pyguide.html
[r]: https://laterality.github.io/styleguide/Rguide.xml
[sh]: https://laterality.github.io/styleguide/shell.xml
[htmlcss]: https://laterality.github.io/styleguide/htmlcssguide.html
[js]: https://laterality.github.io/styleguide/jsguide.html
[angular]: https://laterality.github.io/styleguide/angularjs-google-style.html
[cl]: https://laterality.github.io/styleguide/lispguide.xml
[vim]: https://laterality.github.io/styleguide/vimscriptguide.xml
[cpplint]: https://github.com/google/styleguide/tree/gh-pages/cpplint
[emacs]: https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el
[xml]: https://laterality.github.io/styleguide/xmlstyle.html
[go]: https://golang.org/wiki/CodeReviewComments
[dart]: https://www.dartlang.org/guides/language/effective-dart
[ccl]: https://creativecommons.org/licenses/by/3.0/
