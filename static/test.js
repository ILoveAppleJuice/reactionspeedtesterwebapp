let button = document.querySelector("#button");
let mainDiv = document.querySelector("#testBox")
let preText = document.querySelector("#PreText")
let duringText = document.querySelector("#DuringText");
let promptText = document.querySelector("#PromptText")
let failText = document.querySelector("#FailText")
let afterText = document.querySelector("#AfterText");
let endText = document.querySelector("#EndText")
const urlParams = new URLSearchParams(window.location.search);

let colorData = null;

let result = Cookies.get('result')
if (result != undefined){
    window.location.replace("/completed")
}

console.log(urlParams.get("gender"))
if (urlParams.get("gender") == undefined || urlParams.get("grade") == undefined){
    window.location.replace("/")
}

const results = []
const numTrials = 3
let currTrials = 0

function AddResult(value){
    results.push(value)
}

function DisplayText(name){
    preText.style.display = "none"
    duringText.style.display = "none"
    afterText.style.display = "none"
    promptText.style.display = "none";
    failText.style.display = "none";
    endText.style.display = "none";

    document.querySelector("#"+name).style.display = "block"
}

function HideColor(){
    mainDiv.style["background-color"] = "rgb(99, 99, 99)" //what poop
}

function ShowColor(){
    mainDiv.style["background-color"] = colorData.Hex
}


function GenerateTable(){
    for (let i=0;i<numTrials;i++){
        let tr = document.querySelector("#trTemplate").content.cloneNode(true)
        tr = tr.querySelector("tr")
        tr.querySelector(".trialNum").textContent = i+1
        tr.querySelector(".trialTime").textContent = "-"
        tr.id = "tr"+(i+1)
        document.querySelector("#table").appendChild(tr)
    }
}

function UpdateTableValue(i,val){
    let tr = document.querySelector("#tr"+i);
    tr.querySelector(".trialTime").textContent = val + " ms"
}

GenerateTable()

DisplayText("PreText")

let startTime = 0
let attempt = 0
let currStatus = "PreStart"
function Start(){
    currStatus = "PrePrompt"
    DisplayText("DuringText")
    
    let prevAttempt = attempt
    let randomTime = (Math.random())*4 + 1
    //randomTime = 0
    console.log(randomTime)
    setTimeout(() => {
        if (attempt != prevAttempt){
            return
        }

        currStatus = "ReadyPrompt"
        DisplayText("PromptText")
        startTime = Date.now()

        ShowColor()

    }, randomTime*1000);
}

function GetAverageTime(){
    let total = 0
    for (let i = 0; i < results.length; i++){
        total += results[i]
    }

    if (results.length == 0){
        return 0
    }
    return total/results.length
}


function Submit(){

    const data = {}

    const paramsObject = {};
    for (const [key, value] of urlParams) {
        paramsObject[key] = value;
    }

    data["SubjectInfo"] = paramsObject
    data["Results"] = results

    $.ajax({
        type:"POST",
        url:"/api/submit",
        contentType: "application/json; charset=utf-8",
        data:JSON.stringify(data)
    })
}

function setup(){
    
    console.log(colorData);

    //do set all color span things
    let colorSpans = document.querySelectorAll(".colorSpan");
    for (let i = 0; i < colorSpans.length; i++){
        let e = colorSpans[i]
        e.textContent = colorData.ColorName;
        e.style.color = colorData.Hex
    }

    
    button.onmousedown = function(){
        if (currStatus == "PreStart"){
            Start()

        }else if(currStatus == "PrePrompt"){
            attempt += 1

            currStatus = "PreStart"
            HideColor()
            DisplayText("FailText")
        }else if(currStatus == "ReadyPrompt"){
            HideColor()
            
            let timeTaken = Date.now()-startTime
            AddResult(timeTaken)
            UpdateTableValue(currTrials+1,timeTaken)
            currTrials += 1;
            
            console.log(results)
            if (currTrials >= numTrials){
                document.querySelector("#averageTime").textContent = Math.floor(GetAverageTime()*100)/100
                
                DisplayText("EndText")
                currStatus = "End"
            }else{
                document.querySelector("#timeTaken").textContent = timeTaken
                document.querySelector("#numTrials").textContent = currTrials
                DisplayText("AfterText")
                currStatus = "PostPrompt"
            }
            

        }else if(currStatus == "PostPrompt"){
            HideColor()
            Start()
        }else if(currStatus == "End"){
            Submit();
            Cookies.set('result', GetAverageTime())
            window.location.href = "/completed"
        }
    }
}


let colorJson = Cookies.get("colorData")
console.log(colorJson)
if (colorJson == undefined){
    $.ajax({
        type:"GET",
        url:"/api/getColor",
        success:function(data,success){
            colorData = data;
            Cookies.set("colorData",JSON.stringify(colorData))
            setup()
        }
    })
}else{
    colorData = JSON.parse(colorJson);
    setup()
}


