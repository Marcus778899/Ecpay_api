import logging
import os
from configparser import ConfigParser
from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for
)
from flask_wtf import CSRFProtect
from src import item, module, Params
from request_body_type import MyForm

# init Flask
app = Flask(__name__, template_folder="./templates",static_folder="./static")
config = ConfigParser()
config.read(os.path.join(os.getcwd(),"secretKey.cfg"))
app.config['SECRET_KEY'] = config.get("secret_key", "KEY")
csrf = CSRFProtect(app)

@app.route("/", methods = ['GET'])
def welcome():
    return redirect(url_for("form"))

@app.route("/form", methods=["GET", "POST"])
def form():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(url_for("result"), code=307) # 使用 307 確保 POST 方法被保留
    return render_template("form.html", form=form)

@app.route("/result", methods=["POST"])
def result():
    hostname = request.url
    items = request.form.get("item")
    
    logging.debug(f"Hostname: {hostname}")

    param = Params.get_params()

    ecpay_payment = module.ECPayPaymentSdk(
        MerchantID=param["MerchantID"],
        HashKey=param["HashKey"],
        HashIV=param["HashIV"],
        )
    
    order_params = item.order_param_init(hostname,items)
    order_params.update(item.extend_params_1())
    order_params.update(item.extend_params_2())
    order_params.update(item.extend_params_3())
    order_params.update(item.extend_params_4())

    order_params.update(item.inv_params())

    try:
        final_order_params = ecpay_payment.create_order(order_params)
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # Test environnment
        html = ecpay_payment.gen_html_post_form(action_url, final_order_params)
        return html
    except Exception as e:
        logging.error(f"Error: {e}")
        return render_template("error.html", error=str(e))

# ReturnURL: ecPay Server  
@csrf.exempt
@app.route("/result/receive_result", methods=["POST"])
def receive_result():
    get_request_form = request.form
    print(f"Request form:{get_request_form}")

    result = get_request_form['RtnMsg']
    trade_detail = get_request_form['CustomFiled1']
    print(f"Result: {result} \n 交易細項: {trade_detail}")
    return '1|OK'

#OrderResultURL: ecPay Client
@csrf.exempt
@app.route('/result/trad_result', methods=["Get","POST"])
def end_page():
    if request.method == "GET":
        return "<h1>交易取消</h1>"
    if request.method == "POST":
        try:
            check_mac_value = Params.get_check_mac_value(request.form)
            print(f'trad_result<CheckMacValue>: {check_mac_value}')
            print(f'request.form<CheckMacValue>: {request.form["CheckMacValue"]}')

            if request.form['CheckMacValue'] != check_mac_value:
                trade_status = "交易失敗"
                print("交易失敗")
                logging.debug(f'CheckMacValue: {request.form["CheckMacValue"]}\n交易結果: {trade_status}')
                return "請聯繫賣場人員"
            
            result = request.form['RtnMsg']
            if result == "Succeeded":
                trade_status = "交易成功"
                return render_template("success.html", result=result, trade_status=trade_status)
            else:
                trade_status = "交易失敗"
                return render_template("fail.html", result=result, trade_status=trade_status)
            
        except KeyError as e:
            logging.error(f"Error: {e}")
            return render_template("error.html", error=str(e))
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)
