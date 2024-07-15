import {app} from "../../../scripts/app.js";
import {api} from "../../../scripts/api.js";
import {ComfyWidgets} from "../../../scripts/widgets.js";
import {$el} from "../../../scripts/ui.js";

const styleElement = document.createElement("style"),
    cssCode = "\n    #msgDiv{\n      width:800px;\n      height: 200px;\n      text-align: center;\n      font-size: 30px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      padding-bottom: 40px;\n      color: var(--fg-color);\n    }\n    #qrCode{\n      display: block;\n      width:256px;\n      height:256px;\n      border-radius: 10px;\n    }\n    #qrBox{\n      display: block;\n      text-align: center;\n      display:flex;\n      flex-wrap: wrap;\n      justify-content: center;\n      width: 360px;\n    }\n    #qrDesc{\n      display: block;\n      text-align: center;\n      margin-top: 20px;\n      color: #ffffff;\n      width: 360px;\n    }\n    .codeImg {\n      // display: block;\n      width:256px;\n      height:256px;\n      border-radius: 10px;\n      padding: 10px;\n      border: 2px solid #ffffff;\n    }\n    .codeDesc {\n      display: block;\n      text-align: center;\n      margin-top: 20px;\n      color: #ffffff;\n      width: 360px;\n      font-size: 16px;\n    }\n    .codeDiv {\n      color: #ffffff;\n    }\n    .codeBox {\n      display: flex;\n      text-align: center;\n    }\n    #directions{\n      margin-top: 10px;\n      width: 100%;\n      text-align: left;\n      color: #ffffff;\n      font-size: 8px;\n    }\n    .tech_button {\n      flex:1;\n      height:30px;\n      border-radius: 8px;\n      border: 2px solid var(--border-color);\n      font-size:11px;\n      background:var(--comfy-input-bg);\n      color:var(--error-text);\n      box-shadow:none;\n      cursor:pointer;\n      width: 1rem;\n    }\n    #tech_box {\n      max-height: 80px;\n      display:flex;\n      flex-wrap: wrap;\n      align-items: flex-start;\n    }\n    .uniqueid {\n      display: none;\n    }\n    #showMsgDiv {\n      width:800px;\n      padding: 60px 0;\n      text-align: center;\n      font-size: 30px;\n      color: var(--fg-color);\n    }\n";
styleElement.innerHTML = cssCode, document.head.appendChild(styleElement);
var techsidkey = "techsid" + window.location.port, loading = !1;
const msgBox = $el("div.comfy-modal", {parent: document.body}, []), msgDiv = $el("div", {id: "msgDiv"}, "");

function setCookie(e, t, i = 1) {
    var s = "";
    if (i) {
        var n = new Date;
        n.setTime(n.getTime() + 24 * i * 60 * 60 * 1e3), s = "; expires=" + n.toUTCString()
    }
    document.cookie = e + "=" + (t || "") + s + "; path=/"
}

function getCookie(e) {
    for (var t = e + "=", i = document.cookie.split(";"), s = 0; s < i.length; s++) {
        for (var n = i[s]; " " == n.charAt(0);) n = n.substring(1, n.length);
        if (0 == n.indexOf(t)) return n.substring(t.length, n.length)
    }
    return ""
}

function generateTimestampedRandomString() {
    var uniqueid = (Date.now().toString(36) + Array(3).fill(0).map((() => Math.random().toString(36).substring(2))).join("").substring(0, 18)).substring(0, 32)
    console.log("zhang tao generateTimestamped")
    console.log(uniqueid)
    // return (Date.now().toString(36) + Array(3).fill(0).map((() => Math.random().toString(36).substring(2))).join("").substring(0, 18)).substring(0, 32)
    return uniqueid
}

function showLoading(e = "") {
    hideLoading(), msgDiv.innerText = e || "请稍后...", msgBox.style.display = "block", loading = !0
}

function hideLoading() {
    msgBox.style.display = "none", loading = !1
}

function showToast(e = "", t = 0) {
    t = t > 0 ? t : 2e3, msgDiv.innerText = e || "谢谢", msgBox.style.display = "block", setTimeout((() => {
        msgBox.style.display = "none"
    }), t)
}

msgBox.appendChild(msgDiv), msgBox.style.display = "none", msgBox.style.zIndex = 10001;
var serverUrl = window.location.href;
const qrCode = $el("img", {id: "qrCode", src: "", onerror: () => {}}), qrDesc = $el("div", {id: "qrDesc"}, "请用微信扫码，验证身份..."), qrBox = $el("div", {id: "qrBox"}, [qrCode, qrDesc]);
app.ui.dialog.element.style.zIndex = 10010;
const showMsgDiv = $el("div", {id: "showMsgDiv"}, "请稍后...");

function showCodeBox(e) {
    app.ui.dialog.close();
    let t = [];
    for (let i = 0; i < e.length; i++) t.push($el("div.codeDiv", {}, [$el("img.codeImg", {src: e[i].code}), $el("div.codeDesc", {}, e[i].desc)]));
    const i = $el("div.codeBox", {}, t);
    app.ui.dialog.show(i)
}

function showQrBox(e, t) {
    app.ui.dialog.close(), qrDesc.innerText = t, qrCode.src = e, app.ui.dialog.show(qrBox)
}

function hideCodeBox() {
    app.ui.dialog.close()
}

function showMsg(e) {
    app.ui.dialog.close(), showMsgDiv.innerText = e, app.ui.dialog.show(showMsgDiv)
}

function hideMsg() {
    app.ui.dialog.close()
}

function tech_alert(e) {
    loading = !1, showMsg(e)
}

function getPostData(e) {
    console.log('zhangtao windows getPostData')
    console.log(JSON.stringify(e, null, 2))
    const t = e.output;
    let i = 0, s = {}, n = {}, o = {}, a = [];
    for (const e in t) "sdBxb" == t[e].class_type && (s = t[e].inputs, i++), "SaveImage" == t[e].class_type && (t[e].res_node = e, a.push(t[e]));
    console.log(`i: ${i}`)
    console.log(`s: ${JSON.stringify(s, null, 2)}`)
    console.log(`n: ${JSON.stringify(n, null, 2)}`)
    console.log(`o: ${JSON.stringify(o, null, 2)}`)
    console.log(`a: ${JSON.stringify(a, null, 2)}`)
    if (i > 1) return "工作流中只可以存在1个“SD变现宝”节点";
    if (a.length < 1) return "请确保工作流中有且仅有1个“SaveImgae”或“保存图像”节点，目前有" + a.length + "个";
    if (a.length > 1) return "请确保工作流中有且仅有1个“SaveImgae”或“保存图像”节点，目前有" + a.length + "个";
    if (o.res_node = a[0].res_node, s) {
        if (n.zhutu1 = s["app_img1(optional)"], n.zhutu2 = s["app_img2(optional)"], n.zhutu3 = s["app_img3(optional)"], n.cs_img1 = s["custom_img1(optional)"], n.cs_img2 = s["custom_img2(optional)"], n.cs_img3 = s["custom_img3(optional)"], n.cs_text1 = s["custom_text1(optional)"], n.cs_text2 = s["custom_text2(optional)"], n.cs_text3 = s["custom_text3(optional)"], n.title = s.app_title, n.gn_desc = s.app_desc, n.sy_desc = "作品使用说明", n.server = serverUrl, n.fee = s.app_fee, n.cs_img1_desc = s.custom_img1_desc, n.cs_img2_desc = s.custom_img2_desc, n.cs_img3_desc = s.custom_img3_desc, n.cs_text1_desc = s.custom_text1_desc, n.cs_text2_desc = s.custom_text2_desc, n.cs_text3_desc = s.custom_text3_desc, n.uniqueid = s.uniqueid, o.zhutus = [], n.zhutu1) {
            if ("LoadImage" != t[n.zhutu1[0]].class_type) return "“app_img1”只可以连接“LoadImage”节点";
            t[n.zhutu1[0]].inputs.image && o.zhutus.push(t[n.zhutu1[0]].inputs.image)
        }
        if (n.zhutu2) {
            if ("LoadImage" != t[n.zhutu2[0]].class_type) return "“app_img2”只可以连接“LoadImage”节点";
            t[n.zhutu2[0]].inputs.image && o.zhutus.push(t[n.zhutu2[0]].inputs.image)
        }
        if (n.zhutu3) {
            if ("LoadImage" != t[n.zhutu3[0]].class_type) return "“app_img3”只可以连接“LoadImage”节点";
            t[n.zhutu3[0]].inputs.image && o.zhutus.push(t[n.zhutu3[0]].inputs.image)
        }
        if (o.cs_img_nodes = [], n.cs_img1) {
            if ("LoadImage" != t[n.cs_img1[0]].class_type) return "“custom_img1”只可以连接“LoadImage”节点";
            o.cs_img_nodes.push({node: n.cs_img1[0], desc: n.cs_img1_desc})
        }
        if (n.cs_img2) {
            if ("LoadImage" != t[n.cs_img2[0]].class_type) return "“custom_img2”只可以连接“LoadImage”节点";
            o.cs_img_nodes.push({node: n.cs_img2[0], desc: n.cs_img2_desc})
        }
        if (n.cs_img3) {
            if ("LoadImage" != t[n.cs_img3[0]].class_type) return "“custom_img3”只可以连接“LoadImage”节点";
            o.cs_img_nodes.push({node: n.cs_img3[0], desc: n.cs_img3_desc})
        }
        if (o.cs_text_nodes = [], n.cs_text1) {
            if (!t[n.cs_text1[0]] || void 0 === t[n.cs_text1[0]].inputs || void 0 === t[n.cs_text1[0]].inputs.text) return "“custom_text1”只可以连接“textInput”节点";
            o.cs_text_nodes.push({node: n.cs_text1[0], desc: n.cs_text1_desc})
        }
        if (n.cs_text2) {
            if (!t[n.cs_text2[0]] || void 0 === t[n.cs_text2[0]].inputs || void 0 === t[n.cs_text2[0]].inputs.text) return "“custom_text2”只可以连接“textInput”节点";
            o.cs_text_nodes.push({node: n.cs_text2[0], desc: n.cs_text2_desc})
        }
        if (n.cs_text3) {
            if (!t[n.cs_text3[0]] || void 0 === t[n.cs_text3[0]].inputs || void 0 === t[n.cs_text3[0]].inputs.text) return "“custom_text3”只可以连接“textInput”节点";
            o.cs_text_nodes.push({node: n.cs_text3[0], desc: n.cs_text3_desc})
        }
        return n.title ? (o.title = n.title, n.gn_desc ? (o.gn_desc = n.gn_desc, n.sy_desc ? (o.sy_desc = n.sy_desc, n.server ? (o.server = n.server, n.fee >= 10 ? (o.fee = n.fee, o.uniqueid = n.uniqueid, o.output = t, o) : "“app_fee”不能小于10分，即0.1元") : "程序运行出错，请联系管理员") : "请填写作品使用说明") : "“app_desc”, 不可为空，请填写作品功能介绍") : "“app_title”, 不可为空，请填写作品标题"
    }
}

async function requestExe(e, t) {
    var i = getCookie(techsidkey);
    console.log("zhangtao requestExe() i & techsidkey result")
    console.log(i)
    console.log(techsidkey)
    const s = await api.fetchApi("/manager/tech_zhulu", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({r: e, techsid: i, postData: t})});
    console.log("zhangtao requestExe() fetchApi result")
    console.log(JSON.stringify(s, null, 2))
    if (!s.ok) return void setTimeout((() => {showToast("网络连接出错，请保持电脑联网", 3e3)}), 300);
    return await s.json()
}

async function login(e) {
    let t = await requestExe("comfyui.index.code", {s_key: e});
    return "none" != app.ui.dialog.element.style.display ? t.data.data.techsid.length > 5 ? t.data.data.techsid : (await new Promise((e => setTimeout(e, 800))), await login(e)) : void 0
}

async function request(e, t) {
    showLoading("处理中，请稍后...");
    let i = await requestExe(e, t);
    if (41009 != i.errno) return hideLoading(), i;
    {
        let i = await requestExe("comfyui.index.code", {s_key: ""});
        if (i) {
            if (1 == i.data.data.code) {
                hideLoading(), showQrBox(i.data.data.data, i.data.data.desc);
                let s = await login(i.data.data.s_key);
                return hideCodeBox(), s ? (setCookie(techsidkey, s), await request(e, t)) : void 0
            }
            return void showToast(i.data.data.message)
        }
    }
}

app.registerExtension({
    name: "sdBxb",

    async beforeRegisterNodeDef(e, t, i) {// e:nodeType, t:nodeData, i:app
        if ("sdBxb" === t.name) {
            const t = e.prototype.onNodeCreated;
            e.prototype.onNodeCreated = function () {
                const e = t ? t?.apply(this, arguments) : void 0,
                    s = (this.widgets.findIndex((e => "zhanwei" === e.name)), $el("button.tech_button", {
                        textContent: "点此，工作流转小程序/H5，并获取访问地址",
                        style: {},
                        onclick: async () => {
                            if (!loading) {
                                hideCodeBox();
                                try {
                                    let e = getPostData(await i.graphToPrompt());
                                    console.log("zhangtao resigter() get post data result")
                                    console.log(JSON.stringify(e, null, 2))
                                    if (!e.output) return void tech_alert(e);
                                    try {
                                        let t = await request("comfyui.index.upload", e);
                                        console.log("zhangtao register() get request result")
                                        console.log(JSON.stringify(t, null, 2))
                                        t && (1 == t.data.data.code ? showCodeBox(t.data.data.list) : showMsg(t.data.data.message))
                                    } catch (e) {
                                        hideLoading()
                                    }
                                } catch (e) {
                                    return console.log(e), void tech_alert("获取api数据失败")
                                }
                            }
                        }
                    })),
                    n = $el("div", {id: "directions"}, ["特殊说明：", $el("br"), "1、每创建一个新的“SD变现宝”节点，就对应一个新的作品；", $el("br"), "2、如有问题，请加官方QQ群：967073981，联系作者咨询。", $el("br"), "3、视频教程：https://www.bilibili.com/video/BV1Bsg8eeEjv"]),
                    o = $el("div", {id: "tech_box"}, [s, n]);
                this.addDOMWidget("select_styles", "btn", o);
                const a = document.createElement("input");
                return a.setAttribute("type", "text"), a.setAttribute("list", "uedynamiclist"), a.setAttribute("value", generateTimestampedRandomString()), a.className = "uniqueid", this.addDOMWidget("uniqueid", "input", a, {
                    getValue: () => a.value,
                    setValue(e) {
                        a.value = e
                    }
                }), setTimeout((() => {
                    this.setSize([420, 500])
                }), 200), e
            },

            e.prototype.onRemoved = function () {},

            this.serialize_widgets = !0
        }
    }
});