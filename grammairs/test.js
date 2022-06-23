// async function add(obj, l){ l.push(obj) };

// async function getl(obj, l) { return l[obj] };

// const readline = require('readline');

// const rl = readline.createInterface({
//   input: process.stdin,
//   output: process.stdout
// });


// const ВВОД = async () =>{ //Ввод
//     for await (const line of rl) {
//         return line
//     }
// };

// async function ВЫВОД (obj) { console.log(obj) } ;

// async function add(obj, l){ l.push(obj) }; 

// async function getl(obj, l) { return l[obj] };  

// const readline = require('readline'); 

// const rl = readline.createInterface({   input: process.stdin,   output: process.stdout }); 
// const ВВОД = async () =>{for await (const line of rl) { return line} }; 

// async function ВЫВОД (obj) { console.log(obj) } ;

// async function вставить(obj, t){
//     await add(obj, t)
// }

// async function main(){
    
// }
    
// main();

async function add(obj, l){ l.push(obj) };  
async function getl(obj, l) { return l[obj] };  
const readline = require('readline');  
const rl = readline.createInterface({   input: process.stdin,   output: process.stdout }); 
const ВВОД = async () =>{for await (const line of rl) { return line} };  
async function ВЫВОД (obj) { console.log(obj) } ;

async function main(){ 
    П = [1,4,3,7,2,5,9,10] ;
    П1 = 8 ;
    П50 = П1-1 ;
    П51 = 1 ;
    П2 = 0 ;
    П40 : for ( П2 ; П2 < П50 ; П2 = П2 + П51 ) { 
        П3 = 0 ;
        П52 = П1-1 ; 
        П52 = П52-П2 ; 
        П41 : for ( П3 ; П3 < П52 ; П3 = П3 + П51 ) { 
            П71 = П3+1 ; 
            П61 = await getl( П3 , П ) ; 
            П62 = await getl( П71 , П ) ; 
            if (П61>П62) { 
                П[П3] = П62 ; 
                П[П71] = П61 ; 
            }; 
        }; 
    };
    await ВЫВОД(П) ; 
}; 
main(); rl.close();