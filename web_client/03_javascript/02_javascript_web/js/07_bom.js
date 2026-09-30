/**
 * BOM: navigator
 * - 웹브라우져의 정보
 */
// test1 함수: 브라우저 정보를 확인하는 함수
const test1 = () => {
    console.log(navigator);  // 브라우저 정보가 담긴 navigator 객체 출력
    console.log(navigator.userAgent);  // 브라우저와 OS 식별 문자열 출력
};

/**
 * 주소창관련된 정보 제공
 */
// test2 함수: 현재 주소 정보 확인과 페이지 새로고침을 처리하는 함수
const test2 = () => {
    console.log(location);  // 현재 주소 관련 정보가 담긴 location 객체 출력

    // location.href = 'https://naver.com'; // 페이지이동
    location.reload();  // 현재 페이지 새로고침
};

/**
 * history
 * - 방문기록관련된 정보
 */
// test3 함수: 브라우저 방문 기록 정보를 확인하는 함수
const test3 = () => {
    console.log(history);  // 브라우저 history 객체 출력
};

/**
 * screen
 * - 브라우져가 실행중인 모니터에 대한 정보 제공
 */
// test4 함수: 화면 중앙에 새 창을 여는 함수
const test4 = () => {
    console.log(screen);  // 모니터 정보가 담긴 screen 객체 출력

    const width = 500;  // 새 창 너비
    const height = 300;  // 새 창 높이

    const left = (screen.width - width) / 2 + screen.availLeft;  // 화면 중앙 기준 가로 위치 계산
    const top = (screen.height - height) / 2 + screen.availTop;  // 화면 중앙 기준 세로 위치 계산

    open("", "", `width=${width}, height=${height}, left=${left}, top=${top}`);  // 중앙 위치에 새 창 열기
};