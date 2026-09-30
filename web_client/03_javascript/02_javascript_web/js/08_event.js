/**
 * #btn1 클릭 이벤트 핸들러 
 * @param {#} event 
 */
// test1 함수: 버튼 클릭 이벤트 객체를 확인하는 함수
const test1 = (event) => {
    console.log('#btn1 clicked!');  // 버튼1 클릭 메시지 출력
    console.log(event);  // 이벤트 객체 전체 출력
    console.log(event.target);  // 실제 이벤트가 발생한 요소 출력
};

const $btn2 = document.querySelector('#btn2');  // id가 btn2인 버튼 요소 조회
$btn2.onclick = (e) => {
    console.log('#btn2 clicked!🌽');  // 버튼2 클릭 메시지 출력
    console.log(e);  // 이벤트 객체 출력
};

// addEventListener: 동일이벤트 복수개의 핸들러를 바인딩할 수 있음.
document.querySelector('#btn3').addEventListener('click', (e) => {  // btn3 클릭 이벤트 등록
    console.log('#btn3 clicked!🐸');  // 첫 번째 클릭 핸들러 실행
    // console.log(e);
});
document.querySelector('#btn3').addEventListener('click', (e) => {  // btn3 클릭 이벤트 추가 등록
    console.log('#btn3 clicked!🍩');  // 두 번째 클릭 핸들러 실행
    // console.log(e);
});

document.querySelector('#nickname').addEventListener('focus', (e) => {  // nickname 입력창 focus 이벤트 등록
    console.log('#nickname이 focus 되었습니다.', e);  // focus 발생 로그 출력
});
document.querySelector('#nickname').addEventListener('blur', (e) => {  // nickname 입력창 blur 이벤트 등록
    console.log('#nickname이 blur 되었습니다.', e);  // blur 발생 로그 출력

    const {target: {value}} = e;   // 이벤트 대상의 value 추출
    console.log(value);  // 입력값 출력
    if(!value) {  // 입력값이 비어있으면
        alert('별칭은 필수값입니다.');  // 경고창 출력
        // e.target.focus();
    }
});

/**
 * keydown: 키가 눌리는 순간 발생
 * keypress: 입력키가 문자변환 가능한 경우 발생
 * keyup: 키를 떼면서 발생
 */
document.querySelector('#memo').addEventListener('keydown', (e) => {  // memo 입력창 keydown 이벤트 등록
    console.log('keydown');  // keydown 발생 출력
});
document.querySelector('#memo').addEventListener('keypress', (e) => {  // memo 입력창 keypress 이벤트 등록
    console.log('keypress');  // keypress 발생 출력
});
document.querySelector('#memo').addEventListener('keyup', (e) => {  // memo 입력창 keyup 이벤트 등록
    console.log('keyup');  // keyup 발생 출력
    console.log(e);  // 키보드 이벤트 객체 출력
    console.log(e.target.value);  // 현재 입력된 값 출력

    if (e.keyCode == 13) {  // Enter 키를 누른 경우
        alert(e.target.value);  // 입력값 알림창 출력
        e.target.value = '';  // 입력창 비우기
    }
});
document.querySelector('#memo').addEventListener('compositionend', (e) => {  // 한글 조합 입력 종료 이벤트 등록
    console.log('compositionend', e.data);  // 조합 완료된 문자 출력
});

const $frm = document.signupFrm;  // name이 signupFrm인 form 요소 참조
const $username = $frm.username;  // form 내부 username 요소 참조
const $password = $frm.password;  // form 내부 password 요소 참조
const $confirmPassword = $frm['confirm-password'];  // form 내부 confirm-password 요소 참조

/**
 * 제출 submit 이벤트핸들링
 * - 서버 제출전에 입력한 값에 대한 유효성검사 실시
 * 
 * submit버튼클릭 -> submit이벤트발생 -> submit이벤트핸들러 호출 -> 실제 제출
 * - event.preventDefault() 제출방지처리
 */
$frm.onsubmit = (e) => {
    // 아이디 검사 (4글자 이상)
    if(!/^[a-zA-Z0-9]{4,}$/.test($username.value)) {  // 아이디가 영문/숫자 4자 이상인지 검사
        alert('아이디 영문자/숫자 4글자 이상 입력해주세요.');  // 아이디 오류 메시지 출력
        e.preventDefault();  // 폼 제출 방지
        return;  // 함수 종료
    }

    // 비밀번호 검사 (4글자 이상)
    if(!/^[a-zA-Z0-9]{4,}$/.test($password.value)) {  // 비밀번호가 영문/숫자 4자 이상인지 검사
        alert('비밀번호 영문자/숫자 4글자 이상 입력해주세요.');  // 비밀번호 오류 메시지 출력
        e.preventDefault();  // 폼 제출 방지
        return;  // 함수 종료
    }

    // 비밀번호 확인 검사 (두 비밀번호가 같은지 검사)
    if($password.value !== $confirmPassword.value) {  // 비밀번호와 확인 비밀번호 비교
        alert('두 비밀번호가 일치하지 않습니다.');  // 불일치 메시지 출력
        e.preventDefault();  // 폼 제출 방지
        $password.select();  // 비밀번호 입력값 선택
        return;  // 함수 종료
    }
};

$confirmPassword.onblur = (e) => {
    if($password.value !== $confirmPassword.value) {  // 비밀번호 두 값이 다르면
        alert('두 비밀번호가 일치하지 않습니다.');  // 불일치 메시지 출력
        $password.select();  // 비밀번호 입력값 선택
    }
};

/**
 * 제출성공 함수
 */
// requestSignup 함수: 폼 제출 성공 후 알림과 초기화를 수행하는 함수
const requestSignup = () => {
    alert('폼 제출 성공!');  // 제출 성공 메시지 출력
    $frm.reset();  // 폼 입력값 전체 초기화
};

/**
 * 이벤트 전파 Propagation
 * - bubbling(기본값): 자식객체에서 발생한 이벤트가 부모방향으로 전파되는 것.
 * - capturing
 */
document.querySelector('#bubble1').onclick = (e) => {  // 가장 바깥 div 클릭 이벤트 등록
    console.log('#bubble1 clicked~', e);  // bubble1 클릭 또는 버블링으로 전달된 이벤트 출력
};
document.querySelector('#bubble2').onclick = (e) => {  // 중간 div 클릭 이벤트 등록
    console.log('#bubble2 clicked~', e);  // bubble2 클릭 또는 버블링으로 전달된 이벤트 출력
    e.stopPropagation();  // 여기서 이벤트 전파를 중단해서 상위 요소로 전달되지 않게 함
};
document.querySelector('#bubble3').onclick = (e) => {  // 가장 안쪽 div 클릭 이벤트 등록
    console.log('#bubble3 clicked~', e);  // bubble3 클릭 이벤트 출력
};
document.body.onclick = (e) => {  // body 클릭 이벤트 등록
    console.log('body clicked~', e);  // body까지 전파된 이벤트 출력
};

document.querySelector('#bubble1').onclick = (e) => {
    switch(e.target.id) {  // 실제 클릭된 요소의 id에 따라 분기
        case 'bubble3':
            console.log('#bubble3 clicked!');  // bubble3 클릭 로그 출력
            break;
        case 'bubble2':
            console.log('#bubble2 clicked!');  // bubble2 클릭 로그 출력
            break;
        case 'bubble1':
            console.log('#bubble1 clicked!');  // bubble1 클릭 로그 출력
            break;
    }
};