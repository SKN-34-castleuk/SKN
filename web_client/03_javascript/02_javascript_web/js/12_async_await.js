/**
 * async
 * - 일반함수를 promise처리
 */
document.querySelector('#btn1').onclick = () => {  // btn1 클릭 시 async 함수 반환값 확인
    const promise = foo();  // async 함수 호출 결과는 Promise 객체
    console.log(promise);  // Promise 객체 출력

    promise.then((value) => {  // Promise가 이행되면 실행
        console.log(value);  // 최종 결과값 100 출력
    });
};

// foo 함수: 숫자 100을 Promise 형태로 반환하는 async 함수
const foo = async () => 100;
// const foo = () => new Promise((resolve) => resolve(100));


/**
 * await 
 * - promise에 대해서 작동. 
 * - promise pending -> fulfilled & result 처리를 대기했다 result값을 반환함.
 * - 비동기함수를 동기식으로 처리하는 것처럼 느끼게 됨.
 * - 기본적으로 async함수안에서만 사용가능. (최상위 await도 부분적으로 가능)
 */
document.querySelector('#btn2').onclick = async () => {  // btn2 클릭 시 await 사용 예제 실행
    // bar()
    //     .then((value) => console.log(value));
    
    const value = await bar();  // bar Promise가 끝날 때까지 대기
    console.log(value);  // 완료 후 반환된 🍩 출력
};

// bar 함수: 3초 뒤 🍩를 반환하는 Promise 함수
const bar = () => new Promise((resolve) => {
    setTimeout(() => {  // 3초 뒤 실행
        resolve('🍩');  // Promise 성공 처리
    }, 3000);
});

/**
 * Timer API
 */
document.querySelector('#btn3').onclick = async () => {  // btn3 클릭 시 delay Promise 대기
    const value = await delay(3000)  // 3초 동안 대기
    console.log(value);  // 완료 후 🥕 출력
};

// delay 함수: 지정 시간 뒤 값을 반환하는 Promise 함수
const delay = (millis) => new Promise((resolve) => {
    setTimeout(() => resolve('🥕'), millis);  // millis 뒤 🥕 반환
});

/**
 * DOM
 */
document.querySelector('#btn4').onclick = async () => {  // btn4 클릭 시 외부 스크립트 로드 후 실행
    await loadScript('js/test.js')  // 스크립트가 로드될 때까지 대기
    test();  // 로드 완료 후 test 함수 호출
};

// loadScript 함수: script 태그를 동적으로 생성해 외부 JS를 로드하는 함수
const loadScript = (src) => new Promise((resolve) => {
    const $script = document.createElement('script');  // script 태그 생성
    $script.src = src;  // 불러올 JS 경로 지정
    $script.onload = resolve;  // 로드 완료 시 Promise 성공 처리
    document.body.append($script);  // body에 script 태그 추가
});

document.querySelector('#btn5').onclick = async () => {  // btn5 클릭 시 fetch 요청 실행
    const url = 'https://capybara-659865682482.asia-northeast3.run.app/user';  // 요청할 API 주소

    const response = await fetch(url)  // fetch 응답이 올 때까지 대기
    const data = await response.json()  // 응답 본문을 JSON으로 변환할 때까지 대기
    console.log(data);  // 최종 JSON 데이터 출력
};