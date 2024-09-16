from flask import Flask, jsonify, request, send_file, render_template, send_from_directory
from models import db, Customer
import zipfile
import os
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_POOL_SIZE'] = 10
# app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20

db.init_app(app)

def create_database():
    with app.app_context():
        db.create_all()
        if Customer.query.first() is None:
            print('Data importing.')
            import_data_from_txt('customers.txt')  # 替换为你的TXT文件路径
            print("Data imported successfully.")
        else:
            print("Data already exists, skipping import.")

# @app.route('/')
# def home():
#     return 'Welcome to Customers Management System!'

@app.route('/')
def index():
    return render_template('index.html')

# 导入TXT数据到数据库的脚本
def import_data_from_txt(filepath):
    with app.app_context():
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    # 根据实际TXT文件格式进行分割
                    data = line.strip().split(',')
                    customer = Customer(
                        cust_id=data[0],
                        mobile=data[1],
                        real_name=data[2],
                        province=data[3],
                        city=data[4],
                        address=data[5],
                        login_ip=data[6],
                        login_time=data[7],
                        enabled=int(data[8]),
                        vip_level=int(data[9]),
                        push_ratio = float(data[10]),
                        send_num = int(data[11]),
                        risk_ratio = float(data[12])
                    )
                    db.session.add(customer)
                db.session.commit()
        except Exception as e:
            db.session.rollback()  # 回滚数据库事务
            print(f"Error: {e}")
        finally:
            db.session.close()  # 确保会话关闭以释放资源


# 配置 Flask 以提供 /download 路径下的文件
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    download_dir = '/download'  # 替换为实际的服务器路径
    return send_from_directory(directory=download_dir, path=filename, as_attachment=True)

@app.route('/api/user/export', methods=['POST'])
def export_users():
    params = request.json
    query = Customer.query

    if 'sendLimit' in params:
        query = query.filter(Customer.send_num < params['sendLimit'])

    if 'pushRatio' in params:
        query = query.filter(Customer.push_ratio >= params['pushRatio'] / 100)

    if 'riskRatio' in params:
        query = query.filter(Customer.risk_ratio <= params['riskRatio'] / 100)

    if 'province' in params:
        provinces = params['province'].split(',')
        if params.get('provFilterType') == 'include':
            query = query.filter(Customer.province.in_(provinces))
        elif params.get('provFilterType') == 'exclude':
            query = query.filter(~Customer.province.in_(provinces))

    customers = query.order_by(Customer.cust_id.asc()).all()

    download_dir = '/download'
    os.makedirs(download_dir, exist_ok=True)
    download_path = os.path.join(download_dir, 'custInfo.zip')

    with zipfile.ZipFile(download_path, 'w') as zf:
        with zf.open('客户.txt', 'w') as txt_file:
            for customer in customers:
                txt_file.write(f"{customer.cust_id}\n".encode('utf-8'))

    # 在返回的响应中包含文件路径
    return {"url": f"/download/custInfo.zip"}


# 查询用户接口
@app.route('/api/user/get', methods=['POST'])
def get_user():
    params = request.json
    cust_id = params.get('custId')
    mobile = params.get('mobile')
    send_Limit = params.get('sendLimit')
    pushRatio = params.get('pushRatio')
    riskRatio = params.get('riskRatio')
    if not send_Limit:
        send_Limit = 1000000
    if not pushRatio:
        pushRatio = 0
    if not riskRatio:
        riskRatio = 100
    if cust_id:
        user = Customer.query.filter_by(cust_id=cust_id).first()
    elif mobile:
        user = Customer.query.filter_by(mobile=mobile).first()
    else:
        return jsonify({"error": "custId or mobile must be provided"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 更新营销次数
    user.send_num += 1
    db.session.commit()

    if user.push_ratio >= pushRatio / 100 and user.send_num <= send_Limit and user.risk_ratio <= riskRatio / 100:
        return jsonify({
            "id": user.id,
            "custId": user.cust_id,
            "mobile": user.mobile,
            "realName": user.real_name,
            "province": user.province,
            "city": user.city,
            "address": user.address,
            "loginIp": user.login_ip,
            "loginTime": user.login_time,
            "enabled": user.enabled,
            "vipLevel": user.vip_level,
            "pushRatio": user.push_ratio,
            "sendNum": user.send_num - 1,
            "riskRatio": user.risk_ratio
        })
#
def recreate_database():
    with app.app_context():
        try:
            print("Dropping all tables...")
            db.drop_all()  # 删除现有表
            print("Creating all tables...")
            db.create_all()  # 重新创建表
            print("Database recreated successfully.")
        except Exception as e:
            print(f"Error during database recreation: {e}")


if __name__ == '__main__':
    # recreate_database()  # 重新创建数据库表
    create_database()
    app.run(debug=True, host='0.0.0.0', port=8088)
