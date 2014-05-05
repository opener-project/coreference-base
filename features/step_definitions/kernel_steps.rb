Given /^the kaf file "(.*?)"$/ do |filename|
  @input    = fixture_file(filename)
  @filename = filename
end

Given /^I put them through the kernel$/ do
  tmp_filename = "output_#{rand(1000)}_#{@kaf_filename}_#{@tree_filename}"
  @output      = tmp_file(tmp_filename)
  input        = File.read(@input)
  args         = ["--time_stamp *"]
  output, _    = kernel(args).run(input)

  File.open(@output, 'w') do |handle|
    handle.write(output)
  end
end

Then /^the output should match the fixture "(.*?)"$/ do |filename|
  fixture_output = File.read(fixture_file(filename))
  output         = File.read(@output)

  output.should eql(fixture_output)
end

def fixture_file(filename)
  File.absolute_path("features/fixtures/", kernel_root) + "/#{filename}"
end

def tmp_file(filename)
  tmp_dir = File.expand_path("tmp", kernel_root)
  if File.directory?(tmp_dir)
    return tmp_dir + "/" + filename
  else
    Tempfile.new(filename).path
  end
end
