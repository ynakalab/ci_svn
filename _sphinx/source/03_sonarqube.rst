SonarQubeの設定
###############

ログイン画面
============

======== ==================================
項目     値
======== ==================================
URL      http://sonarqubeのIPアドレス:9000/
Login ID admin
Password admin
======== ==================================

.. image:: ./03_sonarqube/sonarqube01_login.jpeg

で、初回ログイン時に強制的に変更を促されます。

.. image:: ./03_sonarqube/sonarqube02_password_change.jpeg

パスワード変更を行うとホーム画面に遷移します。

.. image:: ./03_sonarqube/sonarqube03_home.jpeg



プロジェクトの登録
==================

| ここでは Subversion リポジトリ名に合わせて **python-test** という名称でジョブを登録します。
| ホーム画面の `Manually` から **Create a project** 画面に遷移します。

.. image:: ./03_sonarqube/sonarqube04_create_a_project.jpeg

`Set Up` ボタンを押下すると下記の画面に遷移します。

.. image:: ./03_sonarqube/sonarqube04_create_a_project2_repository.jpeg

Jenkins と連携する予定ですが、とりあえず `Locally` を選択します。

.. image:: ./03_sonarqube/sonarqube05_provide_a_token.jpeg
.. image:: ./03_sonarqube/sonarqube05_provide_a_token2.jpeg

REST API 用のトークンを発行し、

.. image:: ./03_sonarqube/sonarqube06_project_lang.jpeg

言語を選択し、

.. image:: ./03_sonarqube/sonarqube06_project_lang2.jpeg

| OS を選択すると、soner-scanner コマンドのコマンド引数が出力されます。
| この soner-scanner コマンドをテキストエディタ等にコピーしておきます。
