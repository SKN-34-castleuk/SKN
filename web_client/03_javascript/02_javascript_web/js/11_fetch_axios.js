/**
 * fetch api (자바스크립트 표준)
 * - 비동기 네트워크 요청
 * - XMLHttpRequest객체의 개선버젼. Promise기반 작동.
 */
document.querySelector('#btn1').onclick = (e) => {  // btn1 클릭 시 fetch 요청 실행
    const url = 'https://capybara-659865682482.asia-northeast3.run.app';  // 사용자 정보 요청 주소

    fetch(url)  // GET 요청 전송
        .then((response) => response.json()) // 응답데이터 중 json부분 가져오기  // 응답 본문을 JSON으로 변환
        .then((data) => {
            // console.log(data);
            const {id, company, classroom, cnt} = data;  // 응답 객체에서 필요한 값 구조분해
            document.querySelector('#id').innerHTML = id;  // id 영역에 값 출력
            document.querySelector('#company').innerHTML = company;  // company 영역에 값 출력
            document.querySelector('#classroom').innerHTML = classroom;  // classroom 영역에 값 출력
            document.querySelector('#count').innerHTML = cnt;  // count 영역에 값 출력
        });

};

document.querySelector('#btn2').onclick = (e) => {  // btn2 클릭 시 GitHub 사용자 정보 요청
    const url = 'https://api.github.com/users/capybara-helloworldlabs';  // GitHub API 주소
    
    fetch(url)  // GET 요청 전송
        .then((response) => response.json())  // 응답을 JSON으로 변환
        .then(({avatar_url}) => new Promise((resolve) => {
            console.log(avatar_url);  // 아바타 이미지 주소 출력

            const $img = document.createElement('img');  // img 요소 생성
            $img.src = avatar_url;  // 이미지 주소 지정
            $img.style = 'width: 200px; border-radius: 50%;';  // 이미지 스타일 지정
            $img.onload = () => resolve($img); // 다음 콜백처리  // 이미지 로드 완료 시 img 요소 전달
            // dom tree에 추가
            document.querySelector('.img-wrapper').append($img);  // 화면에 이미지 추가
        }))
        .then(($img) => {
            setTimeout(() => {  // 3초 뒤 실행
                $img.remove();  // 이미지 삭제
            }, 3000);
        })
}

document.querySelector('#btn3').onclick = (e) => {  // btn3 클릭 시 axios 요청 실행
    const url = 'https://api.github.com/users/capybara-helloworldlabs';  // GitHub API 주소

    // get/post/put/patch/delete 전송방식별 메소드
    axios.get(url)  // axios로 GET 요청 전송
        .then(({data: {avatar_url}}) => {
            console.log(avatar_url);  // 아바타 이미지 주소 출력

            const $img = document.createElement('img');  // img 요소 생성
            $img.src = avatar_url;  // 이미지 주소 지정
            $img.style = 'width: 200px; border-radius: 50%;';  // 이미지 스타일 지정
            // dom tree에 추가
            document.querySelector('.axios-img-wrapper').append($img);  // 화면에 이미지 추가
        });
};