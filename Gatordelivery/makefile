SCRIPT = test_case.py

# 定义默认目标
all: run1 run2 run3

# 定义针对每个输入文件的目标
run1:
	@python $(SCRIPT) in1.txt in1_output_file.txt

run2:
	@python $(SCRIPT) in2.txt in2_output_file.txt

run3:
	@python $(SCRIPT) in3.txt in3_output_file.txt

# 定义清理规则
clean:
	@rm -f in1_output_file.txt in2_output_file.txt in3_output_file.txt

.PHONY: all run1 run2 run3 clean
