function reverseString(str) {
  return str.split('').reverse().join('');
}

// Example
console.log(reverseString("hello"));

//function to count characters
function countCharacters(str) {
  return str.length;
}

// Example
console.log(countCharacters("JavaScript")); // 10

//function to capitalize each word in a sentence
function capitalizeWords(sentence) {
  return sentence
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

// Example
console.log(capitalizeWords("hello world from javascript")); // "Hello World From Javascript"

// find min and max Numbers in an array

function findMax(arr) {
  return Math.max(...arr);
}

function findMin(arr) {
  return Math.min(...arr);
}

// Example
console.log(findMax([5, 2, 9, 1, 7])); // 9
console.log(findMin([5, 2, 9, 1, 7])); // 1

// sum an array
function sumArray(arr) {
  return arr.reduce((acc, current) => acc + current, 0);
}

// Example
console.log(sumArray([10, 20, 30, 40])); // 100


function filterArray(arr, conditionFn) {
  return arr.filter(conditionFn);
}

// Example: Filter out odd numbers (keep only even numbers)
console.log(filterArray([1, 2, 3, 4, 5, 6], num => num % 2 === 0)); // [2, 4, 6]


function factorial(n) {
  if (n < 0) return undefined;
  if (n === 0 || n === 1) return 1;
  return n * factorial(n - 1);
}

// Example
console.log(factorial(5)); // 120


function isPrime(num) {
  if (num <= 1) return false;
  for (let i = 2; i <= Math.sqrt(num); i++) {
    if (num % i === 0) return false;
  }
  return true;
}

// Example
console.log(isPrime(11)); // true
console.log(isPrime(4));  // false

function generateFibonacci(terms) {
  if (terms <= 0) return [];
  if (terms === 1) return [0];

  const sequence = [0, 1];
  for (let i = 2; i < terms; i++) {
    sequence.push(sequence[i - 1] + sequence[i - 2]);
  }
  return sequence;
}

// Example: Generate first 7 terms of the Fibonacci sequence
console.log(generateFibonacci(7)); // [0, 1, 1, 2, 3, 5, 8]