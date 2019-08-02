(function () {

    function init(pn) {
        // myAjax(requestUrl, 'GET', null, initCallback)
        $.ajax({
            url: requestUrl,
            data: {'pn':pn},
            success: function (arg) {
                initCallback(arg)
            }
        })
    }

    function bindCheckAllRows() {
        $('#checkall_id').on('click', (e) => {
            $('.selectrow').each((_, e) => {
                if (!e.checked) {
                    if (isEditMode()) {
                        enableEditRow($(e).parent().parent())
                    }
                    e.checked = true
                }
            })
        })
    }

    function bindCheckBox() {
        $('.selectrow').on('click',(e) => {
            let tr = $(e.currentTarget).parent().parent()
            if (isEditMode()) {
                if (e.currentTarget.checked) {
                    enableEditRow(tr)
                } else {
                    disableEditRow(tr)
                }
            }
        })
    }

    function bindCancelAllRows() {
        $('#cancelall_id').on('click', () => {
            $('.selectrow').each((_, e) => {
                if (e.checked) {
                    if (isEditMode()) {
                        disableEditRow($(e).parent().parent())
                    }
                    e.checked = false
                }
            })
        })

    }

    function bindReverseAllRows() {
        $('#reverseall_id').on('click', () => {
            $('.selectrow').each((_, e) => {
                let tr = $(e).parent().parent()
                if (e.checked) {
                    if (isEditMode()) {
                        disableEditRow(tr)
                    }
                } else {
                    if (isEditMode()) {
                        enableEditRow(tr)
                    }
                }
                e.checked = !e.checked
            })
        })

    }

    function bindEditMode() {
        $('#editmode_id').on('click', (e) => {
            if ($(e.currentTarget).attr('edit') === 'true') {
                exitEditMode()
            } else {
                intoEditMode()
            }
        })
    }

    function bindSaveData() {
        $('#savedata_id').on('click', () => {
            if (isEditMode()) {
                exitEditMode()
            }
            let data = packageTbData()
            if (Object.keys(data).length>0){
                myAjax(
                    requestUrl,
                    'POST',
                    {'data': JSON.stringify(data), csrfmiddlewaretoken: csrfToken},
                    function (arg) {
                        $('#tb_head').children().remove()
                        $('#tb_body').children().remove()
                        $('#pager_id').children().remove()
                        init(1)
                    }
                )
            }
        })
    }

    function bindSelectPage() {
        $('.page-link').on('click',(e)=>{
            let pn = e.currentTarget.innerHTML
            init(pn)
        })
    }
    function isEditMode() {
        if ($('#editmode_id').attr('edit') === 'true') {
            return true
        } else {
            return false
        }
    }

    function findSelectedIdxByValue(select, txt) {
        for (let i of $(select).children()) {
            if (i.text === txt) {
                return i.value
            }
        }
    }

    function makeSelectElement(select, td_id) {
        let opts = window['global_dict'][td_id]
        for (let i of opts) {
            let opt = document.createElement('option')
            opt.value = i[0]
            opt.innerHTML = i[1]
            $(select).append(opt)
        }
    }

    function makeCheckbox() {
        let ckb = document.createElement('input')
        ckb.setAttribute('type', 'checkbox')
        $(ckb).addClass('selectrow')
        return ckb
    }

    function packageTbData() {
        let data = {}
        $('#tb_body').find('tr').each((_, row) => {
            // let tr = $(row).parent().parent()
            let tr = $(row)
            let tds = tr.find("[edit='true']")
            let id = tr[0].id
            let obj = {}
            $.each(tds, (_, td) => {
                let txt = ''
                let new_val = td.getAttribute('newvalue')
                let old_val = td.getAttribute('oldvalue')
                if (new_val !== '' && new_val !== old_val) {
                    if (window['global_dict'].hasOwnProperty(td.id)) {
                        for (let item of window['global_dict'][td.id]) {
                            if (item[1] === new_val) {
                                txt = item[0]
                                break
                            }
                        }
                    } else {
                        txt = new_val
                    }
                    obj[td.id] = txt
                    // data[id][td.id] = txt
                }
            })
            if (Object.keys(obj).length>0){
                data[id] = obj
            }
        })
        return data
    }

    function findGlobalKey(choice_key, idx) {
        for (let i of window['global_dict'][choice_key]) {
            if (i[0] === idx) {
                return i[1]
            }
        }
    }

    function disableEditRow(tr) {
        $.each($(tr).children(), (i, td) => {
            if (td.getAttribute('edit')) {
                let t = $(td)
                let child = t.children().first()
                let type = td.getAttribute('type')
                let val = child.val()
                if (type === 'select') {
                    val = child.find("option:selected").text();
                }
                if (val !== td.getAttribute('oldvalue')) {
                    td.setAttribute('newvalue', val)
                }
                t.text(val)
                t.children().remove()
            }
        })
    }

    function enableEditRow(tr) {
        $.each($(tr).children(), (i, td) => {
            if (td.getAttribute('edit')) {
                let type = td.getAttribute('type')
                let t = $(td)
                let txt = t.text()
                t.text('')
                let ele = document.createElement(type)
                if (type === 'select') {
                    makeSelectElement(ele, td.id)
                    ele.value = findSelectedIdxByValue(ele, txt)
                } else {
                    ele.value = txt
                }
                t.append(ele)
            }
        })
    }

    function intoEditMode() {
        let edit = $('#editmode_id')
        edit.attr('edit', 'true')
        edit.text('退出编辑模式')
        $('#tb_body').find(':checked').each((_, t) => {
            enableEditRow($(t).parent().parent())
        })
    }

    function exitEditMode(t) {
        let edit = $('#editmode_id')
        edit.attr('edit', 'false')
        edit.text('进入编辑模式')
        $('#tb_body').find(':checked').each((_, t) => {
            disableEditRow($(t).parent().parent())
        })
    }

    function initGlobalDict(arg) {
        window['global_dict'] = {}
        $.each(arg['global_dict'], (k, v) => {
            window['global_dict'][k] = v
        })
    }

    function createTableHead(arg) {
        let tb_config = arg.tb_config
        let head_tr = document.createElement('tr')
        tb_config.forEach(function (conf) {
            if (conf.display) {
                let th = document.createElement('th')
                th.innerText = conf.title
                $(head_tr).append(th)
            }
        })
        $('#tb_head').append(head_tr)
    }

    function createTableBody(arg) {
        let tb_data = arg.tb_data
        let tb_config = arg.tb_config
        tb_data.forEach((row) => {
            let tr = document.createElement('tr')
            tr.id = row.id
            tb_config.forEach((colConf) => {
                let td = document.createElement('td')
                let kw = Object.assign({}, colConf.text.kwargs)
                let idx = row[colConf.q]
                if (colConf.display) {
                    $.each(kw, (key, val) => {
                        let choice_key = null
                        if (val.substring(0, 2) === "@@") {
                            choice_key = val.substring(2, val.length)
                            td.id = choice_key
                            kw[key] = findGlobalKey(choice_key, idx)
                        } else if (val[0] === '@') {
                            choice_key = val.substring(1, val.length)
                            kw[key] = row[choice_key]
                        }
                        td.id = choice_key
                    })
                    td.innerHTML = colConf.text.content.format(kw)
                    $.each(colConf.attrs, (k, v) => {
                        let txt = v
                        if (typeof(v) === "string") {
                            if (v.substring(0, 2) === '@@') {
                                txt = findGlobalKey(v.substring(2, v.length), idx)
                            } else if (v[0] === '@') {
                                txt = row[v.substring(1, v.length)]
                            }
                        }
                        td.setAttribute(k, txt)
                    })
                    if (colConf.title === '选择') {
                        $(td).append(makeCheckbox())
                    }
                    tr.append(td)
                }
            })
            $('#tb_body').append(tr)
        })

    }

    function createPager(arg) {
        let page_range = arg['page_range']
        let current_page = arg['current_page']
        let total_page = arg['total_page']
        let nav = document.createElement('nav')
        let ul = document.createElement('ul')
        $(nav).append(ul)
        $(ul).addClass('pagination')
        for (let i = page_range[0]; i <=page_range[1] ; i++) {
            let a = document.createElement('a')
            a.innerHTML = i
            $(a).addClass('page-link')
            let li = document.createElement('li')
            $(li).append(a)
            $(li).addClass('page-item')
            if (current_page === i){
                $(li).addClass('active')
            }
            $(ul).append(li)
        }
        $('#pager_id').append(nav)
    }

    function initCallback(arg) {
        console.log(arg)
        initGlobalDict(arg)
        createTableHead(arg)
        createTableBody(arg)
        createPager(arg)
        bindSelectPage()
        bindCheckBox()

    }


    function myAjax(url, method, data, callback) {
        $.ajax({
            url: url,
            method: method,
            data: data,
            dataType: 'json',
            success: function (arg) {
                callback(arg)
            }
        })
    }

    String.prototype.format = function (kw) {
        return this.replace(/{(\w+)}/g, function (km, m) {
            return kw[m]
        })
    }

    jQuery.extend({
        'CRUD': function (url, csrf_token) {
            requestUrl = url
            csrfToken = csrf_token
            init(1)
            bindEditMode()
            bindCheckAllRows()
            bindCancelAllRows()
            bindReverseAllRows()
            bindSaveData()
        }
    })
})()
