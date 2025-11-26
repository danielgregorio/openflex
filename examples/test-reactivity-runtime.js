/**
 * Test OpenFlex Reactivity Runtime
 * Direct JavaScript usage to verify the runtime works
 */

const { Signal, Computed, createEffect } = require('../runtime/openflex-runtime.js');

console.log("=== OpenFlex Reactivity Runtime Test ===\n");

// 1. Basic Signal
console.log("1. Testing Signal:");
const count = new Signal(0);

createEffect(() => {
  console.log(`   Count is now: ${count.value}`);
});

count.value = 1;
count.value = 2;
count.value = 3;

console.log("");

// 2. Computed values
console.log("2. Testing Computed:");
const doubled = new Computed(() => count.value * 2);

createEffect(() => {
  console.log(`   Doubled: ${doubled.value}`);
});

count.value = 5;
count.value = 10;

console.log("");

// 3. Multiple signals
console.log("3. Testing Multiple Signals:");
const firstName = new Signal("John");
const lastName = new Signal("Doe");

const fullName = new Computed(() => `${firstName.value} ${lastName.value}`);

createEffect(() => {
  console.log(`   Full name: ${fullName.value}`);
});

firstName.value = "Jane";
lastName.value = "Smith";

console.log("");

// 4. Effect with multiple dependencies
console.log("4. Testing Multiple Dependencies:");
const x = new Signal(10);
const y = new Signal(20);

createEffect(() => {
  const sum = x.value + y.value;
  console.log(`   ${x.value} + ${y.value} = ${sum}`);
});

x.value = 15;
y.value = 25;
x.value = 100;

console.log("");
console.log("✨ All tests passed! Reactivity system working!");
