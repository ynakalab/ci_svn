####################
SonarQube の手動実行
####################

SonarQube の手動実行の流れは下記のようになります。

.. actdiag::

    actdiag {
        create_project -> coding -> pytest -> sonar-scanner -> confirm;
        lane user {
            label = "User"
            coding [label = "コーディング"];
            pytest [label = "テストの実行"];
            sonar-scanner [label = "sonar-scanner の実行"];
        }
        lane sonarqube {
            label = "SonarQube"
            create_project [label = "プロジェクト作成"];
            confirm [label = "テストの結果確認"];
        }
    }


#. **プロジェクト作成**

    :doc:`./03_sonarqube` 参照

#. **コーディング**

    とりあえず四則演算を行うコード (calc.py) とテストコード (test_calc.py) を用意します。

    * ソースファイルの配置

        .. code-block:: text

            /home/ubuntu/python-test
            |-- calc.py
            |-- test_calc.py


    * calc.py

        .. code-block:: python

            class Calc:
                def add(self, a: int, b: int) -> int:
                    return a + b

                def sub(self, a: int, b: int) -> int:
                    return a - b

                def multiply(self, a: int, b: int) -> int:
                    return a * b

                def divide(self, a: int, b: int) -> int:
                    return a // b

    * test_calc.py

        .. code-block:: python

            from calc import Calc

            def test_add():
                c = Calc()
                assert c.add(3, 4) == 7
                assert c.sub(3, 4) == -1
                assert c.multiply(3, 4) == 12
                assert c.divide(3, 4) == 0


#. **テストの実行**

    * **pytest のインストール**

        .. code-block:: bash

            pip3 install --upgrade pytest pytest-cov

    * **pytest の実行 / カバレッジレポート作成**

        .. code-block:: bash

            PYTHONPATH=./ pytest -v --cov=./ --cov-report=xml

#. **sonar-scanner の実行**

    * **SonarScanner のインストール**

        `SonarQube のドキュメントサイト <https://docs.sonarqube.org/9.6/analyzing-source-code/scanners/sonarscanner/>`_ から実行環境 OS 用の SonarScanner をダウンロードします。

        .. code-block:: bash

            wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
            unzip sonar-scanner-cli-4.8.0.2856-linux.zip -d $HOME/bin
            export PATH=$HOME/bin/sonar-scanner-4.8.0.2856-linux/bin:$PATH

    * **sonar-scanner の実行 (コマンドオプション)**

        .. code-block:: bash

            sonar-scanner \
                -Dsonar.projectKey=python-test \
                -Dsonar.sources=. \
                -Dsonar.host.url=http://sonarqube:9000 \
                -Dsonar.login=sqp_c5ddeae3aa6f601562ed8a9986da16fc20c0359b

#. **テストの結果確認**

    | SonarQube のプロジェクトページを参照すると、カバレッジやよろしくないコーディングをやらかしてる箇所を指摘してくれます。
    | ただ、これまでの手順ではカバレッジが更新されません。


========================================
カバレッジ込みのテストレポートを生成する
========================================

* **ツールのインストール**

    .. code-block:: bash

        pip3 install --upgrade coverage

* **カバレッジレポートの作成**

    .. code-block:: bash

        coverage erase
        coverage run --source=./ -m pytest -v
        coverage report
        coverage xml -i

* **sonar-scanner の実行**

    .. code-block:: bash

        sonar-scanner \
            -Dsonar.projectKey=python-test \
            -Dsonar.sources=./ \
            -Dsonar.host.url=http://sonarqube:9000 \
            -Dsonar.login=sqp_c5ddeae3aa6f601562ed8a9986da16fc20c0359b \
            -Dsonar.exclusions=**/test_*.py,**/*xml,**/*pyc \
            -Dsonar.language=py \
            -Dsonar.python.coverage.reportPaths=coverage.xml \
            -X

    コマンドオプションに `-X` を付けると、標準出力に詳細なログが出力されるようになります。

sonar-project.properties
************************

| sonar-project.properties ファイルにコマンドオプションを書いておくと、オプション無しの sonar-scanner でテスト結果を SonarQube に送信できます。
| コマンドオプションの先頭の `-D` を削除した文字列を sonar-project.properties に書くだけです。

* sonar-project.properties の作成

    .. code-block:: bash

        sonar.projectKey=python-test
        sonar.sources=./
        sonar.host.url=http://sonarqube:9000
        sonar.login=sqp_c5ddeae3aa6f601562ed8a9986da16fc20c0359b
        sonar.exclusions=**/test_*.py,**/*xml,**/*pyc
        sonar.language=py
        sonar.python.coverage.reportPaths=coverage.xml

* sonar-scanner の実行

    .. code-block:: bash

        sonar-scanner -X


======
その他
======

カバレッジを HTML 形式で確認する
********************************

.. code-block:: bash

    PYTHONPATH=./ pytest -v --cov=./ --cov-report=html

を実行後、`./htmlcov/index.html` を参照するとカバレッジや実行したコード／していないコードをブラウザで確認できます。
