/**
 * 동기 Synchronous: 짝을 맞춘다. (함수호출-리턴과 그 다음실행의 짝을 맞춘다)
 * 비동기 Asynchronous: 짝을 맞추지 않는다. (함수호출-리턴과 그 다음실행의 짝을 맞추지 않는다.)
 * 
 * js runtime(node, web browswer)는 기본적으로 싱글쓰레드로 작업한다.
 * 1. 비동기처리가 필요한 경우 Web API 영역에 등록
 * 2. 실행시기가 오면 callback queue에 등록
 * 3. EventLoop이 주기적으로 확인해서, callstack이 비면, callback queue의 작업을 callstack 추가/실행
 */
document.querySelector('#btn1').addEventListener('click', () => {  // btn1 클릭 이벤트 등록
    // 동기처리
    const value = foo();  // foo 함수 실행 후 반환값 저장
    console.log(value);  // 동기 처리 결과 300 출력
    
    // 비동기처리
    let value2;  // 아직 값이 없는 변수 선언
    const timeoutId = setTimeout(() => {  // 1초 뒤 실행될 비동기 작업 등록
        value2 = 200;  // 1초 후 value2에 값 저장
        console.log(value2);  // 1초 후 200 출력
    }, 1000);
    console.log(value2); // undefined  // setTimeout 이전이라 아직 undefined 출력
});

// foo 함수: 숫자 300을 반환하는 함수
const foo = () => 300;

/**
 * DOM 처리는 비동기 작업이다.
 */
document.querySelector('#btn2').onclick = (e) => {  // btn2 클릭 이벤트 등록
    loadScript('js/test.js', () => {  // 외부 스크립트 파일을 동적으로 로드
        // callback함수
        test();  // 스크립트 로드 완료 후 test 함수 실행
    });
    // test();
};

// loadScript 함수: 외부 스크립트를 읽어온 뒤 콜백 함수를 실행하는 함수
const loadScript = (src, callback) => {
    const script = document.createElement('script');  // script 태그 생성
    script.src = src;  // 불러올 스크립트 경로 지정
    script.onload = callback;  // 스크립트 로드 완료 시 콜백 실행
    document.body.append(script);  // body에 script 태그 추가
};

document.querySelector('#btn3').onclick = () => {  // btn3 클릭 이벤트 등록
    const $box = document.querySelector('div.box');  // class가 box인 div 요소 조회
    $box.style.backgroundColor = 'red';  // 처음 배경색을 빨강으로 변경
    setTimeout(() => {  // 1초 뒤 실행
        $box.style.backgroundColor = 'orange';  // 주황색으로 변경
        setTimeout(() => {  // 다시 1초 뒤 실행
            $box.style.backgroundColor = 'yellow';  // 노란색으로 변경
            setTimeout(() => {  // 다시 1초 뒤 실행
                $box.style.backgroundColor = 'green';  // 초록색으로 변경
                setTimeout(() => {  // 다시 1초 뒤 실행
                    $box.style.backgroundColor = 'blue';  // 파란색으로 변경
                    setTimeout(() => {  // 다시 1초 뒤 실행
                        $box.style.backgroundColor = 'navy';  // 남색으로 변경
                            setTimeout(() => {  // 다시 1초 뒤 실행
                            $box.style.backgroundColor = 'purple';  // 보라색으로 변경
                        }, 1000);
                    }, 1000);
                }, 1000);
            }, 1000);
        }, 1000);
    }, 1000);
};