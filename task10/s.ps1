msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
	$id = (Get-Process msiexec).id
	echo $id[0] 
	Wait-Process -Id $id[0]
