class A{
    constructor(mda){
        this.mda = mda
        this.c = []
    }

    add(element) {
        this.c.push(element)
    }
}

let a = new A(1)
let b = new A(2)

a.add(b)

delete a

console.log('123')