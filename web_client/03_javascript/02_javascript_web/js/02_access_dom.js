/*
    ID로 태그찾기 : getElementById
     - 1개의 태그객체 또는 null 반환
*/
const test1 = () => {
    const li1 = document.getElementById('li1');  // id가 li1인 요소 찾기
    console.log(li1);  // 요소 객체
    console.dir(li1);  // 요소의 속성 구조

    console.log(li1.innerText);  // 요소의 텍스트 내용

    // 존재하지 않는 id인 경우
    const notExist = document.getElementById('asdsfjdsiofjasdioj');
    console.log(notExist);
};

/*
    태그명으로 찾기 : getElementsByTagName
     - 검색된 모든 태그를 배열로 반환
     - 해당 태그가 존재하지 않으면 빈 배열이 반환
*/
const test2 = () => {
    const lis = document.getElementsByTagName('li');  // 모든 li 태그 조회
    console.log(lis);  // li 목록 조회

    for (let tag of lis) {
        console.log(tag.innerText);  // li의 텍스트 출력
        tag.style.backgroundColor = 'hotpink';  // 배경색
        tag.style.color = 'white';  // 글씨색
    }

    // 존재하지 않는 태그인 경우
    const brs = document.getElementsByTagName('br');  // 모든 br 태그 조회
    console.log(brs);  // br 목록 조회
};

/*
    클래스명으로 찾기 : getElementsByClassName
*/
const test3 = () => {
    const group1 = document.getElementsByClassName('group1');  // class가 group1인 요소들 조회
    console.log(group1);  // 요소 목록 조회
    for (let tag of group1) {  // 각 요소 순회
        tag.innerHTML += '[group1]';  // 기존 내용 뒤에 문자열 추가
    }
};

/*
    CSS선택자로 찾기
     - querySelector() : 선택자와 일치하는 한개의 요소 반환 (없으면 null 반환)
     - querySelectorAll() : 선택자와 일치하는 모든 요소를 배열로 반환 (없으면 빈 배열)
*/
const test4 = () => {
    const li3 = document.querySelector('#li3');  // id가 li3인 요소 1개 조회
    li3.style.fontSize = '24px';  // 글씨 크기 변경

    const group2 = document.querySelector('.group2');  // class가 group2인 첫번째 요소 조회
    console.log(group2);
};

const test5 = () => {
    const group2 = document.querySelectorAll('.group2');  // class가 group2인 모든 요소 조회
    console.log(group2);

    // 각 요소 순회
    group2.forEach((tag) => {
        console.log(tag);
        tag.innerHTML = tag.innerHTML.replace('HelloJS', '안녕! 자바스크립트!')  // 문자열 치환
    });
};

/*
    name속성으로 찾기 : getElementsByName
     - input[name]
*/
const test6 = () => {
    const hobbies = document.getElementsByName('hobby'); // name 속성이 hobby인 요소들 조회
    console.log(hobbies);

    let hobbyChecked = '';         // 선택된 취미 저장용 문자열
    hobbies.forEach((tag) => {
        console.log(tag.checked);  // 체크여부 출력
        if (tag.checked) {
            hobbyChecked += tag.value + ' '  // value 값을 문자열에 추가
        }
    });
    alert(`[${hobbyChecked.trim()}]를 선택하셨습니다.`);
};

// 체크박스 전체 선택/해제 처리 함수
const test7 = () => {
    const hobbyAll = document.querySelector("#all")  // id가 all인 요소 선택

    const hobbies = document.getElementsByName('hobby');
    hobbies.forEach((tag) => {
        tag.checked = hobbyAll.checked;
    });
};

// 입력창의 값을 읽어서 출력하는 함수
const test8 = () => {
    const user_name = document.querySelector("#name");  // id가 name인 요소 조회
    alert(user_name.value);  // 해당 요소의 value 속성 값
};

// range 입력값을 화면에 표시하는 함수
const test9 = () => {
    const score = document.querySelector('#score');  // 점수 range 요소 조회
    const display_score = document.querySelector('#display-score');  // 점수 표시 영역

    display_score.innerHTML = score.value;
};