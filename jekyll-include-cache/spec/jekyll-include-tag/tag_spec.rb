# frozen_string_literal: true

RSpec.describe JekyllIncludeCache::Tag do
  let(:tag_name) { "include_cached" }
  let(:file_path) { "foo.html" }
  let(:params) { "foo=bar foo2=bar2" }
  let(:markup) { "#{file_path} #{params}" }

  let(:overrides) { {} }
  let(:site) { fixture_site("site", overrides) }
  let(:environments) { {} }
  let(:outer_scope) { {} }
  let(:registers) { { :site => site } }
  let(:context) { Liquid::Context.new(environments, outer_scope, registers) }
  let(:parse_context) { Liquid::ParseContext.new }

  subject { described_class.send(:new, tag_name, markup, parse_context) }
  let(:cache) { JekyllIncludeCache.cache }
  let(:path) { subject.send(:path, context) }
  let(:parsed_params) { subject.parse_params(context) }
  let(:cache_key) { subject.send(:key, path, parsed_params) }

  it "determines the path" do
    expected = File.expand_path "../fixtures/site/_includes/foo.html", __dir__
    expect(path).to eql(expected)
  end

  context "building the key" do
    it "builds the key" do
      key = subject.send(:key, "foo.html", "foo" => "bar", "foo2" => "bar2")
      expect(key).to eql("19f48d1dba832dec7442c3ed57ecd9ed")
    end

    it "builds the key based on the path" do
      key = subject.send(:key, "foo2.html", "foo" => "bar", "foo2" => "bar2")
      expect(key).to eql("1397798e1ca375c42640615904c18a8c")
    end

    it "builds the key based on the params" do
      key = subject.send(:key, "foo2.html", "foo" => "bar")
      expect(key).to eql("2e357f2d61c19e041986cb8409cc0e25")
    end
  end

  context "rendering" do
    before { subject.render(context) }
    let(:rendered) { subject.render(context) }

    it "renders" do
      expect(rendered).to eql("Some content\n")
    end

    it "caches the include" do
      expect(cache.key?(cache_key)).to be_truthy
      expect(cache[cache_key]).to eql("Some content\n")
    end

    context "with the cache stubbed" do
      before { allow(subject).to receive(:key).and_return(cache_key) }
      before { cache[cache_key] = "Some other content\n" }
      let(:cache_key) { "asdf" }

      it "returns the cached value" do
        expect(rendered).to eql("Some other content\n")
      end
    end
  end

  context "with an invalid include" do
    let(:file_path) { "foo2.html" }

    it "raises an error" do
      expect { subject.render(context) }.to raise_error(IOError)
    end
  end
end
