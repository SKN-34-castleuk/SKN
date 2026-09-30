/**
 * DOM은 Node로 구성되어 있다.
 * - TextNode
 * - CommentNode
 * - ElementNode(태그객체)
 */

// test1 함수: DOM 요소를 선택해서 노드 구조를 확인하는 함수
const test1 = () => {
    // $로 시작하는 변수는 태그객체임을 명시
    const $sample = document.querySelector('#sample');  // id가 sample인 요소 조회
    console.dir($sample);  // 요소의 상세 속성과 노드 구조 출력
};

/**
 * DOM Tree 탐색
 * 
 * Node제공 속성 (모든 노드 대상)
 * 1. 자식탐색 firstChild, lastChild, childNodes
 * 2. 부모탐색 parentNode
 * 3. 형제탐색 nextSibling, previousSibling
 * 
 * Element제공 속성 (Element만 탐색)
 * 1. 자식탐색 firstElementChild, lastElementChild, children
 * 2. 부모탐색 parentElement
 * 3. 형제탐색 nextElementSibling, previousElementSibling
 * 
 */
// test2 함수: 자식 요소들을 탐색해서 스타일을 변경하는 함수
const test2 = () => {
    const $src = document.querySelector('.wrapper');  // class가 wrapper인 부모 요소 조회
    console.log($src);  // 부모 요소 출력

    // const $target = $src.firstElementChild;
    // const $target = $src.lastElementChild;
    // console.log($target);
    // $target.style.color = 'magenta';

    const $target = $src.children;  // 자식 Element 목록 조회
    console.log($target);  // HTMLCollection 출력

    // 진짜배열로 변환: Array.from(), [...유사배열]
    Array.from($target).forEach((tag) => {  // 배열로 변환 후 각 자식 요소 순회
    // [...$target].forEach((tag) => {
        tag.style.color = 'magenta';  // 각 자식 요소 글자색 변경
    });
};

/**
 * 부모방향 탐색
 */
// test3 함수: 부모 요소를 따라 올라가서 스타일을 변경하는 함수
const test3 = () => {
    const $src = document.querySelector('#p4');  // id가 p4인 요소 조회
    const $target = $src.parentElement.parentElement;  // 부모의 부모 요소 조회
    console.log($target);  // 찾은 부모 요소 출력
    $target.style.backgroundColor = 'yellowgreen';  // 배경색 변경
};

/**
 * 형제방향 탐색
 * - previousElementSibling
 * - nextElementSibling
 */
// test4 함수: 형제 요소를 탐색해서 스타일을 변경하는 함수
const test4 = () => {
    const $src = document.querySelector('#p3');  // id가 p3인 요소 조회
    // const $target = $src.previousElementSibling.previousElementSibling;
    const $target = $src.nextElementSibling;  // 다음 형제 요소 조회
    $target.style.textDecoration = 'underline';  // 밑줄 스타일 적용
};