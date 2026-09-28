/*
js 함수 작성법
1. 함수선언식 Function Declaration
    - hoisting 처리
2. 함수표현식 Function Expression
    - hoisting 처리 안됨

hoisting이란? 끌어올려져 처리.
*/

foo();
// console.log(k);  // var로 hosting되어 undefined
// console.log(m);  // let은 hosting되지 않아 오류 발생

function foo() {
    console.log('foooooooo');
}

var k = 10;  // var로 선언하면 호스팅됨
let m = 20;  // let은 선언 전 접근 불가

/*
함수 표현식 : 익명함수를 변수에 대입 
*/
// bar()  // 함수 표현식은 hosting되지않음
const bar = function () {
    console.log('baaaaaaaaaaaaaaar')
};
bar();

/**
 * IIFE:
 * - Immediately Invoked Function Expression
 * - 함수를 정의/호출하는 방식
 * - 전역변수 대신 지역변수를 선언하고, 보호하는 방식
 */
// 즉시 실행 함수
(function() {
    console.log('IIFE 테스트');
})();

(function(name) {
    console.log(`Hello ${name}`);
})('홍길동');

// IIFE 내부 지역변수는 외부에서 참조 불가
(() => {
    let pet_name = '햄토리';      // IIFE 내부 지역변수
})();
// console.log(pet_name);  // 참조오류

let app_name = 'MyFantasticApp';

app_name = 'YourFantasticApp'
console.log(app_name)

/*
    매개변수 / 매개인자가 불일치해도 오류가 발생하지 않음
*/
const test1 = function(a, b) {
    console.log(a, b);
    console.log(arguments)  // 실제로 전달된 모든 인자
}

test1(10, 20);
test1(10);
test1();
test1(10, 20, 30);

/*
    모든 함수는 리턴값을 갖는다.
    return절을 명시하지 않으면, undefined 반환
*/
const test2 = function() {}
console.log(test2());

/**
 * 화살표함수 Arrow Function
 * - 파이썬 lambda와 같이 함수를 간결하게 작성하는 문법
 */
// 일반함수
const f1 = function(a, b) {
    console.log(a, b);
    return a + b;
}
console.log(f1(10, 20))

// 화살표 함수
const f2 = (a, b) => a + b;
console.log(f2(10, 20))

const f3 = (a, b) => console.log(a, b);
f3(10, 20)

/**
 * 파이썬 *, **: 
 * - packing: def foo(*args), def foo(**kwargs) 매개변수
 * - unpacking: foo(*mylist), foo(**mydict) 매개인자
 * 
 * JS ...
 * - 나머지파라미터(rest parameter): 함수선언자리에서 매개인자 묶어 처리. 매개변수(공간)
 * - 전개연산자(spread operator): 배열/객체의 요소를 나열. 매개인자(값)
 */

const test3 = (year, ...names) => {
    console.log(names, typeof(names));

    for(let name of names) {
        console.log(name);
    }
};

test3(1990, '홍길동')
test3(2000, '홍길동', '신사임당')
test3(2010, '홍길동', '신사임당', '이순신')

const names = ['홍길동', '신사임당'];
test3(2026, names);     // 배열 자체를 하나의 인자로서 전달
test3(2026, ...names);  // 전개연산자를 통해 배열 요소를 펼쳐서 전달

// 전개연산자
(() => {
    const a = [1, 2, 3];
    const b = ['a', 'b', 'c'];

    const c = a.concat(b);  // concat으로 배열 합치기
    console.log(c);

    const d = [...a, ...b];  // 전개연산자로 배열 합치기
    console.log(d);
})();

/**
 * 자바스크립트 함수는 1급시민객체이다!
 * 
 * 1급시민객체란?
 * - 무명의 리터럴로 생성가능해야 한다. 
 * - 변수 또는 자료구조(배열/객체)에 저장가능해야 한다.
 * - 함수의 매개인자로 사용이 가능해야 한다.
 * - 함수의 리턴값으로 사용이 가능해야 한다.
 */

// 함수를 변수처럼 저장하고 호출
const test4 = (k) => {
    console.log(`😍😀😝 ${k}`)
}
test4('안녕!');

// 함수를 다른 변수에도 저장 가능
const test5 = test4;
test5('반가워~');

// test4 식별자, test4 함수 사용 객체
const obj_funcs = {
    test4: test4
}
obj_funcs['test4']('abc');  // 객체 속성으로 정의된 함수 호출

const funcs = [test1, test2, test3, test4]
funcs[3]('이것도 되나?')  // 배열에서 함수를 꺼내어 호출

// 함수의 매개인자로 다른 함수를 받아 사용
const runner = (f, n) => {
    for(let i = 0; i < n; i++) {
        f('안녕!');
    }
}
runner(test4, 3);

// 함수를 반환하는 클로저 형태의 함수
const test6 = (emoji) => { 
    return () => {
        console.log(emoji)  // 외부 함수에서의 emoji 값을 내부에서 사용
    };
};
const dog_emoji = test6('🐶')
dog_emoji();
const cat_emoji = test6('🐈‍⬛')
cat_emoji();

// 디저트 종류에 따라 문장을 만들어주는 함수를 반환
const getDessert = (dessert) => {
    return (name) => `${name}이/가 ${dessert}을/를 먹어요~`;
};

const getCake = getDessert('🍰')
const getDonut = getDessert('🍩')

console.log(getCake('철수'))
console.log(getDonut('은희'))

// 고차함수
const getDessert2 = (dessert) => (name) => `${name}이/가 ${dessert}을/를 먹어요~`;
const getCarrot = getDessert2('🥕');
console.log(getCarrot('토끼'));

const friends = ['길동', '순신', '관순'];
const getCorn = getDessert('🌽');  // 옥수수 문장 생성 함수

// 각 친구에 대한 문장 생성
friends.forEach((friends) => console.log(getCorn(friends)));

// 문장들을 새 배열로 하나씩 적용해서 생성
const results = friends.map((friend) => getCorn(friends));
console.log(results);