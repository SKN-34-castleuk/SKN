// forEach를 사용해 배열의 각 요소를 문장 형태로 출력하는 함수
function test1(){
    const fruits = ['apple', 'banana', 'orange'];  // 과일 배열 생성
    fruits.forEach((fruit) => {
        console.log(`I like ${fruit}`);  // 각 과일명을 문장으로 출력
    });
}
test1();

// map을 사용해 세금이 포함된 새 가격 배열을 만드는 함수
function test2(){
    const prices = [1000, 2500, 3000];  // 가격 배열 생성
    const taxed_prices = prices.map((price) => price * 1.1);  // 각 가격에 10% 세금 추가
    console.log(taxed_prices);  // 새 배열 출력
}
test2();

// filter를 사용해 10보다 큰 숫자만 추출하는 함수
function test3(){
    const numbers = [5, 12, 8, 130, 44];  // 숫자 배열 생성
    const result = numbers.filter((number) => number > 10);  // 10보다 큰 값만 추출
    console.log(result);  // 결과 배열 출력
}
test3();

// reduce를 사용해 배열의 총합을 구하는 함수
function test4(){
    const numbers = [1, 2, 3, 4, 5];  // 숫자 배열 생성
    const sum = numbers.reduce((acc, cur) => acc + cur, 0);  // 누적합 계산
    console.log(sum);  // 총합 출력
}
test4();

// filter와 map을 함께 사용해 짝수의 제곱값 배열을 만드는 함수
function test5(){
    const numbers = [1, 2, 3, 4, 5, 6];  // 숫자 배열 생성
    const result = numbers
        .filter((number) => number % 2 == 0)  // 짝수만 추출
        .map((number) => number ** 2);  // 각 짝수를 제곱
    console.log(result);  // 결과 배열 출력
}
test5();

// reduce를 사용해 문자열 배열을 한 문장으로 결합하는 함수
function test6(){
    const words = ['JavaScript', 'is', 'fun'];  // 문자열 배열 생성
    const sentence = words.reduce((acc, cur) => acc + ' ' + cur);  // 공백을 포함해 문자열 결합
    console.log(sentence);  // 최종 문장 출력
}
test6();