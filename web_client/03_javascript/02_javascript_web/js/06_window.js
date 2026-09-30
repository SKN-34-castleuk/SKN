/**
 * window객체
 * - 브라우져 탭별로 존재하는 최상위 객체
 * - DOM (Document Object Model): document
 * - BOM (Browswer Object Model): navigator, history, location, screen
 * - Javascript (내장객체)
 * - 편의메소드: open(), alert(), console등
 */
// test1 함수: window 객체와 브라우저 창 크기를 확인하는 함수
const test1 = () => {
    console.log(window);  // 현재 브라우저의 최상위 window 객체 출력
    // this용법: 전역 this는 window객체를 가리킨다.
    console.log(this);  // 전역 this 출력

    console.log(window.outerWidth, window.outerHeight);  // 브라우저 전체 창 크기 출력
    console.log(window.innerWidth, window.innerHeight);  // 실제 문서 표시 영역 크기 출력
};

/**
 * open함수: 새창을 띄우는 함수
 */
// test2 함수: 새 창을 열고 일정 시간 뒤 닫는 함수
const test2 = () => {
    // open(url, name, spec) -> window객체 반환
    // const newWindow = open('01_js_on_web.html', 'js_on_web', 'width=500, height=300, top=400, left=400');
    const newWindow = open('01_js_on_web.html', 'js_on_web', '');  // 새 브라우저 창 열기
    console.log(newWindow);  // 새로 열린 window 객체 출력
    console.log(newWindow.opener);  // 현재 창을 연 부모 window 출력

    setTimeout(() => {  // 3초 뒤 실행
        // newWindow.alert('🐸🐸🐸');
        newWindow.close();  // 새 창 닫기
    }, 3000);

};

// test3 함수: 확인 창 결과에 따라 다른 동작을 수행하는 함수
const test3 = () => {
    const bool = confirm('정말 회원탈퇴하시겠습니까?');  // 사용자 확인 여부 받기
    console.log(bool);  // 확인 결과 true/false 출력

    if (bool) {  // 확인을 누른 경우
        alert('회원탈퇴를 진행합니다. 다음에 또 뵙겠습니다.');  // 안내 메시지 출력
    }
};

// test4 함수: prompt로 입력값을 받아 인사 메시지를 출력하는 함수
const test4 = () => {
    const name = prompt('당신의 이름은 무엇입니까?', '홍길동');  // 이름 입력 받기
    console.log(name);  // 입력값 출력

    if (name) {  // 값이 입력된 경우
        alert(`반갑습니다. ${name}님~ 🐸`);  // 이름을 포함한 인사 출력
    }
    else {  // 취소했거나 빈 값인 경우
        alert('유효한 이름을 입력해주세요.');  // 안내 메시지 출력
    }
};

/**
 * Timer API
 * - setTimeout() - clearTiemeout()
 * - setInterval() - clearInterval()
 */
// test5 함수: 일정 시간이 지난 뒤 한 번만 실행되는 타이머 함수
const test5 = () => {
    const timeoutId = setTimeout(() => {  // 3초 뒤 한 번 실행
        alert('🐸🐸🐸');  // 알림창 출력
    }, 3000);
    console.log('timeoutId =', timeoutId);  // 생성된 timeout 식별자 출력
};

// test6 함수: 일정 시간마다 반복 실행되는 타이머 함수
const test6 = () => {
    let i = 0;  // 카운트 변수 선언
    const intervalId = setInterval(() => {  // 1초마다 반복 실행
        i++; // ++i, i++ (전위/후위 증감연산자)  // 카운트 1 증가
        console.log(i);  // 현재 카운트 출력
    }, 1000);
    console.log('intervalId =', intervalId);  // 생성된 interval 식별자 출력
};

// 즉시실행함수: 현재 시각을 초시계처럼 화면에 출력하는 함수
(() => {
    setInterval(() => {  // 1초마다 반복 실행
        // 매초 Date객체를 생성하고, 시분초를 화면에 출력
        const d = new Date()  // 현재 날짜와 시간 객체 생성
        const $clock = document.querySelector('#clock');  // 시계를 표시할 요소 조회
        const f = (n) => n > 10 ? n : '0' + n;  // 한 자리 숫자면 앞에 0을 붙이는 함수
        $clock.innerHTML = `${f(d.getHours())}:${f(d.getMinutes())}:${f(d.getSeconds())}`;  // 현재 시분초를 화면에 출력
    }, 1000);
})();