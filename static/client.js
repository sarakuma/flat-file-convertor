//global variables
var form = document.querySelector("form")
var mainRadioBtns = document.querySelectorAll('input[name="init-choice"]')
var dtodAttrsExist
var dtoexcelAttrsExist

//handle radio button click events
mainRadioBtns.forEach((radio) => {

       radio.checked = false
       radio.addEventListener("click", () => {

           if (radio.value === "dtod") {

                if (!dtodAttrsExist) {

                    let dtodAttrs = document.createElement("fieldset")
                    dtodAttrs.innerHTML = "<legend>Enter the below details</legend>"
                    dtodAttrs.id = "files-attrs"
                    form.appendChild(dtodAttrs)
                    let uploadAttrs = document.createElement("fieldset")
                    uploadAttrs.innerHTML = `<legend>Input file attributes</legend>
                                            <input type=radio name="indelim" id="incsv" value="csv" required>Comma delimited
                                            <input type=radio name="indelim" id="intsv" value="tsv">Tab delimited
                                            <input type=radio name="indelim" id="inpsv" value="psv">Pipe delimited
                                            <input type=radio name="indelim" id="inesv" value="~sv">Tilde delimited<br>
                                            <label id="label-for-file" for="infil">Select a file to transform</label>
                                            <input type=file id="infil" name="infil" required><br>`
                    dtodAttrs.appendChild(uploadAttrs)
                    let dwnldAttrs = document.createElement("fieldset")
                    dwnldAttrs.innerHTML = ` <legend>Output file attributes</legend>
                                            <input type=radio name="outdelim" id="outcsv" value="csv">Comma delimited
                                            <input type=radio name="outdelim" id="outtsv" value="tsv" required>Tab delimited
                                            <input type=radio name="outdelim" id="outpsv" value="psv">Pipe delimited
                                            <input type=radio name="outdelim" id="outesv" value="~sv">Tilde delimited`
                    dtodAttrs.appendChild(dwnldAttrs)
                    let submitBtn = document.createElement("div")
                    submitBtn.id = "submit-btn"
                    submitBtn.innerHTML = '<input type="submit" value="Transform" required>'
                    dtodAttrs.appendChild(submitBtn)
                    dtodAttrsExist = true
    
                    var incsv = document.querySelector("#incsv")
                    var intsv = document.querySelector("#intsv")
                    var inpsv = document.querySelector("#inpsv")
                    var inesv = document.querySelector("#inesv")
                    var outcsv = document.querySelector("#outcsv")
                    var outtsv = document.querySelector("#outtsv")
                    var outpsv = document.querySelector("#outpsv")
                    var outesv = document.querySelector("#outesv")
                    var label4fil = document.querySelector("#label-for-file")
                    var infil = document.querySelector("#infil")
    
                    incsv.addEventListener("click", () => {
                        outcsv.disabled = true
                        outpsv.disabled = false
                        outtsv.disabled = false
                        outesv.disabled = false
                        label4fil.textContent = "Select a file to transform"
                        infil.value = ""
                    })
                    inpsv.addEventListener("click", () => {
                        outpsv.disabled = true
                        outcsv.disabled = false
                        outtsv.disabled = false
                        outesv.disabled = false
                        label4fil.textContent = "Select a file to transform"
                        infil.value = ""
                    })
                    intsv.addEventListener("click", () => {
                        outtsv.disabled = true
                        outpsv.disabled = false
                        outcsv.disabled = false
                        outesv.disabled = false
                        label4fil.textContent = "Select a file to transform"
                        infil.value = ""
                    })
                    inesv.addEventListener("click", () => {
                        outesv.disabled = true
                        outpsv.disabled = false
                        outtsv.disabled = false
                        outcsv.disabled = false
                        label4fil.textContent = "Select a file to transform"
                        infil.value = ""
                    })
    
                    outcsv.addEventListener("click", () => {
                        incsv.disabled = true
                        inpsv.disabled = false
                        intsv.disabled = false
                        inesv.disabled = false
                    })
                    outpsv.addEventListener("click", () => {
                        inpsv.disabled = true
                        incsv.disabled = false
                        intsv.disabled = false
                        inesv.disabled = false
                    })
                    outtsv.addEventListener("click", () => {
                        intsv.disabled = true
                        inpsv.disabled = false
                        incsv.disabled = false
                        inesv.disabled = false
                    })
                    outesv.addEventListener("click", () => {
                        inesv.disabled = true
                        inpsv.disabled = false
                        intsv.disabled = false
                        incsv.disabled = false
                    })
    
                    infil.addEventListener("change", () => {
                        label4fil.textContent = infil.files[0].name
    
                    })
                    
                }

                if (dtoexcelAttrsExist) {
                    var filesAttrs = document.querySelector("#files-attrs")
                    if (typeof filesAttrs !== undefined) {
                        filesAttrs.remove()
                        dtoexcelAttrsExist = false
                    }
                }

           } else if(radio.value === "dtoexcel") {

                if (dtodAttrsExist) {
                    var filesAttrs = document.querySelector("#files-attrs")
                    if (typeof filesAttrs !== undefined) {
                        filesAttrs.remove()
                        dtodAttrsExist = false
                    }
                }

                if (!dtoexcelAttrsExist) {

                    let dtoexcelAttrs = document.createElement("fieldset")
                    dtoexcelAttrs.innerHTML = "<legend>Enter the below details</legend>"
                    dtoexcelAttrs.id = "files-attrs"
                    form.appendChild(dtoexcelAttrs)
                    let uploadAttrs = document.createElement("fieldset")
                    uploadAttrs.innerHTML = `<legend>Input file attributes</legend>
                                            <input type=radio name="indelim" id="incsv" value="csv" required>Comma delimited
                                            <input type=radio name="indelim" id="intsv" value="tsv">Tab delimited
                                            <input type=radio name="indelim" id="inpsv" value="psv">Pipe delimited
                                            <input type=radio name="indelim" id="inesv" value="~sv">Tilde delimited<br>
                                            <label id="label-for-file" for="infil">Select a file to transform</label>
                                            <input type=file id="infil" name="infil" required><br>`
                    dtoexcelAttrs.appendChild(uploadAttrs)

                    let submitBtn = document.createElement("div")
                    submitBtn.id = "submit-btn"
                    submitBtn.innerHTML = '<input type="submit" value="Transform" required>'
                    dtoexcelAttrs.appendChild(submitBtn)
                    dtoexcelAttrsExist = true

                    var infil = document.querySelector("#infil")
                    var label4fil = document.querySelector("#label-for-file")
                    
                    infil.addEventListener("change", () => {
                        label4fil.textContent = infil.files[0].name
    
                    })
                }
           
           } else {
               if (dtodAttrsExist) {
                   var filesAttrs = document.querySelector("#files-attrs")
                    if (typeof filesAttrs !== undefined) {
                        filesAttrs.remove()
                        dtodAttrsExist = false
                    }
               }

               if (dtoexcelAttrsExist) {
                var filesAttrs = document.querySelector("#files-attrs")
                 if (typeof filesAttrs !== undefined) {
                     filesAttrs.remove()
                     dtoexcelAttrsExist = false
                 }
            }

           }
       })
})

// form.addEventListener("submit", () => {
//     console.log(`form submitted`)
    
// })

//trigger a function (whenever DOM loads) to check the progress of the download every 10s
window.onload = function() {
    setInterval(checkProgress, 10000)
  };

//function to check the progress of the download
var checkProgress = () => {
    let dataRows = document.querySelectorAll("tbody > tr")

    if (dataRows) {
        dataRows.forEach((dataRow) => {
        let rowID = dataRow.id
        rowID = parseInt(rowID.replace("dwnld-link", ""))
        let url = `http://localhost:9001/download/progress/${rowID}`
        let xhr = new XMLHttpRequest()
        xhr.open("GET", url)
        xhr.setRequestHeader("Content-Type", "application/json")
        xhr.send(null)
        xhr.onreadystatechange = (resp) => {
            if(xhr.readyState === 4 && xhr.status === 200) {
                let data = xhr.responseText
                let progid = document.querySelector(`#prog${rowID}`)
                tranObj = JSON.parse(data)
                let currVal = parseInt(tranObj[rowID]["currVal"])
                let filename = tranObj[rowID]["filename"]
                if (currVal >= 99) {
                    let anchor = document.querySelector("tbody > tr > td:last-child > a")
                    anchor.href = `http://localhost:9001/download-file/${filename}`
                }
                progid.value = currVal
            }
        }
        
    })

    }

}  