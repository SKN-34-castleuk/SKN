/**
 * DOM객체의 style속성을 변경하면, inline-style속성을 변경하는 것과 같다.
 */
// test1 함수: 요소의 인라인 스타일을 직접 변경하는 함수
const test1 = () => {
    const $first = document.querySelector('#first');  // id가 first인 요소 조회
    $first.style.backgroundColor = 'black';  // 배경색을 검정색으로 변경
    $first.style.color = 'white';  // 글자색을 흰색으로 변경
};

/**
 * 클래스 속성을 통한 styling
 */
// checkSubject 함수: 체크 여부에 따라 클래스명을 추가/제거하는 함수
const checkSubject = ($checkbox) => {
    const checked = $checkbox.checked;  // 체크박스의 체크 상태 저장
    // console.log(checked);

    // 부모태그 td 가져오기
    const $td = $checkbox.parentElement;  // 체크박스의 부모 td 요소 조회
    // console.log($td);

    if(checked) {  // 체크된 경우
        $td.classList.add('on');  // on 클래스 추가
    }
    else {  // 체크 해제된 경우
        $td.classList.remove('on');  // on 클래스 제거
    }
};