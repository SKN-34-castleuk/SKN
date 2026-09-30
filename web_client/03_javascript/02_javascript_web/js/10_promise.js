/**
 * Promise객체
 * - 비동기작업(producing code) + 콜백(consuming code)를 명쾌히 작성하도록 도와주는 객체
 * 
 * 두개의 상태
 * - status: pending -> fullfiled / rejected (resolve 호출 / reject 호출)
 * - result: undefined -> value / error객체
 * 
 * Promise는 두개의 callback을 가진다.
 * - resolve 정상처리된 경우 실행할 callback
 * - reject 오류가 발생한 경우 실행할 callback
 */
document.querySelector('#btn1').onclick = (e) => {  // btn1 클릭 시 Promise 생성 및 실행
    const promise = new Promise((resolve, reject) => {
        // 짝수 생성기 (난수)
        const n = Math.trunc(Math.random() * 100 + 1); // 1 ~ 100사이 난수  // 1부터 100 사이의 난수 생성
        console.log(`난수가 생성되었습니다: ${n}`);  // 생성된 난수 출력

        try {
            if (n % 2 == 0) {  // 짝수인 경우
                resolve(n); // Promise#result: n  // 성공 상태로 전환하고 난수 전달
            }
            else {  // 홀수인 경우
                throw new Error('홀수라서 실패!');  // 에러 발생
            }
        } catch (e) {
            reject(e); // Promise#result: e(에러객체)  // 실패 상태로 전환하고 에러 전달
        }
    });
    console.log(promise);  // 생성된 Promise 객체 출력

    // 콜백 작성
    promise.then((n) => {
        // resolve 콜백
        console.log(`🥳🥳🥳 짝수를 뽑았습니다: ${n} 🥳🥳🥳`);  // 성공 시 짝수 결과 출력
    }, (err) => {
        // reject 콜백
        console.error(err);  // 실패 시 에러 출력
    });
};

/**
 * Timer API + Promise
 * - producing 코드: Timer API
 * - cosuming 코드: Timer API에 전달된 callback 함수
 */
document.querySelector('#btn2').onclick = () => {  // btn2 클릭 시 delay Promise 실행
    delay(3000).then((value) => {
        console.log('🥑🥑🥑', value);  // 3초 뒤 전달된 값 출력
    });
};

// delay 함수: 지정한 시간 뒤 resolve 되는 Promise를 반환하는 함수
const delay = (millis) => new Promise((resolve, reject) => {
    setTimeout(() => {  // millis 밀리초 뒤 실행
        resolve('🎈🎈🎈');  // 성공 값 전달
    }, millis);
});

/**
 * DOM + Promise
 * - producing: script 생성/로드
 * - consuming: test함수 호출
 */
document.querySelector('#btn3').onclick = () => {  // btn3 클릭 시 외부 스크립트 로드
    loadScript('js/test.js').then((value) => {
        test();  // 스크립트 로드 완료 후 test 함수 실행
    });
};

// loadScript 함수: script 태그를 생성해 외부 JS를 로드하는 함수
const loadScript = (src) => new Promise((resolve, reject) => {
    const script = document.createElement('script');  // script 태그 생성
    script.src = src;  // 불러올 JS 파일 경로 지정
    script.onload = resolve;  // 로드 완료 시 resolve 실행
    // script.onload = () => resolve();
    document.body.append(script);  // body에 script 태그 추가
});

/**
 * Promise Chain
 * - then구문은 다시 Promise를 반환하므로, 연속적인 사용이 가능
 */
document.querySelector('#btn4').addEventListener('click', () => {  // btn4 클릭 시 Promise Chain 실행
    new Promise((resolve) => {
        resolve(2);  // 처음 값 2로 시작
    }).then((value) => {
        return value * 2; // result=4인 Promise객체 반환  // 2를 2배 해서 다음 then으로 전달
    }).then((value) => {
        console.log(value);  // 최종 결과 4 출력
    });
});

const $box = document.querySelector('div.box');  // box 요소 조회
document.querySelector('#btn5').addEventListener('click', () => {  // btn5 클릭 시 배경색 순차 변경 시작
    $box.style.backgroundColor = 'red';  // 처음 배경색을 빨강으로 설정
    changeBGColor('orange', 1000)
        .then(() => changeBGColor('yellow', 1000))  // 1초 후 노랑으로 변경
        .then(() => changeBGColor('green', 1000))  // 1초 후 초록으로 변경
        .then(() => changeBGColor('blue', 1000))  // 1초 후 파랑으로 변경
        .then(() => changeBGColor('navy', 1000))  // 1초 후 남색으로 변경
        .then(() => changeBGColor('purple', 1000))  // 1초 후 보라로 변경
});

// changeBGColor 함수: 지정한 시간 뒤 박스 배경색을 바꾸는 Promise 함수
const changeBGColor = (color, millis) => new Promise((resolve) => {
    setTimeout(() => {  // millis 밀리초 뒤 실행
        $box.style.backgroundColor = color;  // 박스 배경색 변경
        resolve();  // 작업 완료 처리
    }, millis);
});