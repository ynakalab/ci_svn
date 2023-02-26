########
環境設定
########

.. note::

    1 台 の Linux PC に Docker をインストールして、Docker コンテナで構成することを前提としています。

==============================
このドキュメントで作成するもの
==============================

Subversion、SonarQube、Jenkins を連携して、ソースコードのコミットを契機に Jenkins で自動テストを実行し、SonarQube でコード解析するソースコード管理システムを作成します。

.. actdiag::

    actdiag {
        create_sonarqube_project -> create_jenkins_project -> create_svn_repository -> jenkinsfile -> coding -> commit -> test -> confirm_sonarqube;

        lane user {
            label = "User"
            coding [label = "コーディング"];
        }
        lane subversion {
            label = "Subversion"
            create_svn_repository [label = "Subversion リポジトリ作成"];
            commit;
        }
        lane jenkins {
            label = "Jenkins"
            create_jenkins_project [label = "Jenkins プロジェクト作成"];
            jenkinsfile [label = "Jenkins ファイル作成"];
            test [label = "自動テスト"];
        }
        lane sonarqube {
            label = "SonarQube"
            create_sonarqube_project [label = "SonarQube プロジェクト作成"];
            confirm_sonarqube [label = "自動テスト結果確認"];
        }
    }


============
Linux の設定
============

| /etc/sysctl.conf に下記の内容を追加するか、下記の内容で /etc/sysctl.d/99-sonarqube.conf を作成します。
| 反映には OS の再起動が必要です。

.. code-block::bash

    fs.file-max=65536
    vm.max_map_count=262144

コマンドをコピペする場合は、以下のように入力します。

.. code-block:: bash

    sudo bash -c 'echo -e "fs.file-max=65536\nvm.max_map_count=262144" > /etc/sysctl.d/99-sonarqube.conf'
    sudo reboot


=============
Docker の準備
=============

* `Debian Linux <https://docs.docker.com/engine/install/debian/>`_

    .. code-block:: bash

        sudo apt-get install -y ca-certificates curl gnupg lsb-release
        curl -fsSL https://download.docker.com/linux/debian/gpg | \
            sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
            $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose

    .. code-block:: bash

        sudo systemctl enable docker
        sudo systemctl start docker

    .. code-block:: bash

        sudo usermod -aG docker ユーザID

* `Ubuntu Linux <https://docs.docker.com/engine/install/ubuntu/>`_

    .. code-block:: bash

        sudo apt-get update
        sudo apt-get install \
                apt-transport-https \
                ca-certificates \
                curl \
                gnupg \
                lsb-release
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
        echo \
            "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
            $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose

    .. code-block:: bash

        sudo systemctl enable docker
        sudo systemctl start docker

    .. code-block:: bash

        sudo usermod -aG docker ユーザID

* Rocky Linux

    公式手順は紹介されていないのですが、`Install Docker Engine on CentOS <https://docs.docker.com/engine/install/centos/>`_ と同じみたいです。

    * docker-ce

        .. code-block:: bash

            sudo yum install -y yum-utils
            sudo yum-config-manager \
                --add-repo \
                https://download.docker.com/linux/centos/docker-ce.repo
            sudo yum install docker-ce docker-ce-cli containerd.io

            sudo systemctl enable docker
            sudo systemctl start docker

    * `docker-ce <https://docs.docker.com/compose/install/#install-compose-on-linux-systems>`_

        .. code-block:: bash

            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
            sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
            docker-compose --version


=============
Docker の起動
=============

Docker 関連ファイル
*******************

`ci_subversion.zip <../_static/resource/ci_subversion.zip>`_

* ファイル構成

    .. code-block:: text

        |--_jenkins
        | |--Dockerfile
        | |--sonar-scanner-cli-4.8.0.2856-linux.zip
        |--_svn
        | |--Dockerfile
        | |--etc.apache2.sites-enabled
        | | |--svnroot.conf
        | | |--viewvc.conf
        | |--etc.viewvc
        | | |--viewvc.conf
        | |--index.html
        |--docker-compose.yml


その他の準備
************

* jenkins_home ディレクトリの作成

    .. code-block:: bash

        sudo mkdir -p ./volume/jenkins_home
        sudo chown 1000:1000 ./volume/jenkins_home

* sonarqube ディレクトリの作成

    .. code-block:: bash

        sudo mkdir -p ./volume/sonarqube/{conf,data,extensions,logs}
        sudo chmod 777 ./volume/sonarqube/{conf,data,extensions,logs}


Docker コンテナの起動
*********************

| 　jenkins コンテナでは jenkins_home ディレクトリにコンテナ外のディレクトリをマウントするようにしないと、コンテナの再作成の度に初期設定からやり直すことになります。ただ、最初からコンテナ外ディレクトリのマウント設定をしておくと、空のディレクトリをマウントしてしまうためコンテナの起動に失敗します。
| 　回避方法として、一旦、コンテナ外ディレクトリのマウント無しで jenkins コンテナを起動し、jenkins_home ディレクトリをコンテナの外にコピーしてから、コピーしたディレクトリをマウントする手順で起動することで、jenkins コンテナ再作成問題をごまかします。

#. docker-compose.yml を一部編集して起動

    volumes の設定をコメントにして起動する。

    .. code-block:: yaml

        jenkins:
            build: ./_jenkins
            container_name: jenkins
            hostname: jenkins
            restart: always
            # ここをコメントにして一旦起動する
            #volumes:
            #    - ./volume/var.jenkins_home:/var/jenkins_home
            ports:
                - 8080:8080
            links:
                - svn
                - sonarqube


#. jenkins コンテナの `/var/jenkins_home` ディレクトリをコンテナから取り出し、`./volume/var.jenkins_home` にコピーする

    .. code-block:: bash

        docker cp jenkins:/var/jenkins_home ./volume/


#. docker-compose.yml を戻して起動する

    volumes の設定をコメントを解除する。

    .. code-block:: yaml

        jenkins:
            build: ./_jenkins
            container_name: jenkins
            hostname: jenkins
            restart: always
            volumes:
                - ./volume/var.jenkins_home:/var/jenkins_home
            ports:
                - 8080:8080
            links:
                - svn
                - sonarqube

#. コピーしたファイルの権限を調整する

    .. code-block:: bash

        sudo chown -R 1000:1000 ./volume/jenkins_home
