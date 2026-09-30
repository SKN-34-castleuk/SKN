/**
 * DOM 요소를 추가/수정/삭제
 * 
 * 1. 텍스트로 처리
 * 2. 태그객체로 처리
 * 
 * innerHTML
 * - (getter) 자식 HTML을 포함해서 가져오기
 * - (setter) HTML태그가 포함된 문자열인 경우, HTML로써 파싱처리
 */
const $foo = document.querySelector('#foo');  // id가 foo인 요소 조회
const $bar = document.querySelector('#bar');  // id가 bar인 요소 조회
const $target = document.querySelector('#target');  // id가 target인 요소 조회

// test1 함수: innerHTML로 HTML 구조를 읽고 복사하는 함수
const test1 = () => {
    console.log($foo.innerHTML);  // foo의 내부 HTML 출력
    $bar.innerHTML = $foo.innerHTML;  // foo의 내부 HTML을 bar에 그대로 복사
};

/**
 * innerText
 * - (getter) 자식 HTML을 제외한 문자열을 가져온다.
 * - (setter) HTML포함 문자열을 전달해도, HTML 파싱처리 하지 않음.
 */
// test2 함수: innerText로 텍스트만 읽고 넣는 함수
const test2 = () => {
    console.log($foo.innerText); // textContent와 동일  // foo의 텍스트만 출력
    $bar.innerText = $foo.innerHTML;  // HTML 문자열도 문자 그대로 출력되게 설정
};

/**
 * outerHTML
 * - (getter): 태그 자신을 포함한 문자열 반환
 * - (setter): 태그 자신을 덮어쓰기 처리
 */
// test3 함수: outerHTML로 요소 전체를 확인하고 교체하는 함수
const test3 = () => {
    console.log($foo.outerHTML);  // foo 태그 자신을 포함한 HTML 출력
    $foo.outerHTML = `<p id='koo'>🥑🥑🥑</p>`  // foo 요소 자체를 새로운 p 태그로 교체
};


/**
 * <!-- beforebegin: 이전 형제요소 추가 -->
 * <p> 
 * <!-- afterbegin: 첫번째 자식요소 추가 -->
 *  foo 
 * <!-- beforeend: 마지막 자식요소 추가 -->
 * </p>
 * <!-- afterend: 다음 형제요소 추가 -->
 */
// test4 함수: target 요소 앞에 형제 요소를 추가하는 함수
const test4 = () => {
    $target.insertAdjacentHTML('beforebegin', '<span>🎈</span>')  // target 이전에 span 추가
};
// test5 함수: target 요소 내부 맨 앞에 자식 요소를 추가하는 함수
const test5 = () => {
    $target.insertAdjacentHTML('afterbegin', '<span>🎈</span>')  // target 내부 첫 번째 자식으로 span 추가
};
// test6 함수: target 요소 내부 맨 뒤에 자식 요소를 추가하는 함수
const test6 = () => {
    $target.insertAdjacentHTML('beforeend', '<span>🎈</span>')  // target 내부 마지막 자식으로 span 추가
};
// test7 함수: target 요소 뒤에 형제 요소를 추가하는 함수
const test7 = () => {
    $target.insertAdjacentHTML('afterend', '<span>🎈</span>')  // target 다음에 span 추가
};

/**
 * Element 생성
 * - textNode: document.createTextNode(text)
 * - ElementNode: docuemnt.createElement(tagName)
 */
// test8 함수: 새 요소와 텍스트 노드를 만들어 화면에 추가하는 함수
const test8 = () => {
    const $h3 = document.createElement('h3');  // h3 요소 생성
    const $text = document.createTextNode('안녕, HTML');  // 텍스트 노드 생성
    $h3.appendChild($text);  // h3에 텍스트 노드 추가
    console.log($h3);  // 생성된 h3 요소 출력

    const $area = document.querySelector('#area');  // id가 area인 요소 조회
    $area.appendChild($h3); // 기존 DOM Tree 추가 및 화면 렌더  // area 하위에 h3 추가

    $h3.addEventListener('click', () => {  // h3 클릭 이벤트 등록
        alert('😺😺😺');  // 클릭 시 알림창 출력
    });
};

// test9 함수: 이미지 요소를 만들어 속성을 지정한 뒤 화면에 추가하는 함수
const test9 = () => {
    const $img = document.createElement('img'); // <img src='' alt=''/>  // img 요소 생성
    $img.src = '../../assets/image/hyunta.jpg';  // 이미지 경로 지정
    $img.width = 200  // 이미지 너비 지정
    $img.style.borderRadius = '50%';  // 원형 이미지처럼 보이게 설정
    $img.style.margin = '10px';  // 바깥 여백 설정

    const $area = document.querySelector('#area');  // id가 area인 요소 조회
    $area.appendChild($img);  // area 하위에 이미지 추가
};

/**
 * remove(): 태그 자기자신 삭제
 */
// test10 함수: 선택한 요소 자기 자신을 삭제하는 함수
const test10 = () => {
    const $target = document.querySelector('#good-morning');  // id가 good-morning인 요소 조회
    $target.remove();  // 해당 요소 삭제
};

/**
 * removeChild(child): 자식노드 제거
 */
// test11 함수: 부모 요소의 자식 노드를 삭제하는 함수
const test11 = () => {
    const $parent = document.querySelector('#messages');  // id가 messages인 부모 요소 조회
    // const $target = document.querySelector('#good-morning');
    // $parent.removeChild($target);

    // 모든 자식노드 삭제
    while($parent.firstChild){  // 첫 번째 자식이 있는 동안 반복
        console.log($parent.firstChild);  // 삭제 대상 자식 노드 출력
        $parent.removeChild($parent.firstChild);  // 첫 번째 자식 노드 삭제
    }
};

/**
 * innerHTML 통해서 삭제
 */
// test12 함수: innerHTML을 비워서 자식 요소를 모두 삭제하는 함수
const test12 = () => {
    const $parent = document.querySelector('#messages');  // id가 messages인 요소 조회
    console.log($parent.innerHTML);  // 기존 내부 HTML 출력
    $parent.innerHTML = '';  // 내부 내용을 비워 자식 요소 전체 삭제
};

/**
 * 기존요소 이동
 * - 기존요소를 새부모 밑에 추가
 */
// test13 함수: 기존 요소를 다른 부모 요소 아래로 이동시키는 함수
const test13 = () => {
    const $target = document.querySelector('#good-morning');  // 이동할 요소 조회
    const $newParent = document.querySelector('#another-messages');  // 새 부모 요소 조회
    $newParent.appendChild($target);  // 기존 요소를 새 부모 아래로 이동
};