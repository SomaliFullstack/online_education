function fizzBuzz(num) {
    if (num % 3 === 0 && num % 5 === 0) {
        return "FizzBuzz";
    } else if (num % 3 === 0) {
        return "Fizz";
    } else if (num % 5 === 0) {
        return "Buzz";
    } else {
        return num;
    }
}


console.log(fizzBuzz(3));  // "Fizz"
console.log(fizzBuzz(5));  // "Buzz"
console.log(fizzBuzz(15)); // "FizzBuzz"
