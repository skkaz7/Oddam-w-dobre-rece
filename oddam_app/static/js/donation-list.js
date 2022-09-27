const btn = document.querySelectorAll('button[id="btn1"]')
const lis = document.querySelectorAll('li[id="li1"]')
const buttony = []
btn.forEach(x => {
    buttony.push(x)
})

console.log(btn)
console.log(lis)
console.log(buttony)
lis.forEach(((x, index) => {
        if (!buttony[index]) {
            x.style.opacity = "0.25"
        }
    })
)
