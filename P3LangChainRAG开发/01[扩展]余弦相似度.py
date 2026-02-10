


def get_dot(vec_a, vec_b):
    """计算两个向量的点积,2个向量必须是同维度的"""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must be of the same dimension")
    dot_sum = 0
    for a, b in zip(vec_a, vec_b): #zip将多个可迭代对象（如列表、元组、向量等）“打包” 成一个可迭代的 “配对元组序列”
        dot_sum += a * b
    return dot_sum

def get_norm(vec):
    #计算单个向量的模长：对向量的每个数字平方后求和，再开平方
    sum_square = 0
    for v in vec:
        sum_square += v * v
    return sum_square ** 0.5

def cosine_similarity(vec_a, vec_b):
    """计算两个向量的余弦相似度"""
    dot_product = get_dot(vec_a, vec_b)
    norm_a = get_norm(vec_a)
    norm_b = get_norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        raise ValueError("One of the vectors is zero-length")
    return dot_product / (norm_a * norm_b)

if __name__ == "__main__":
    vec_a = [1, 2, 3]
    vec_b = [4, 5, 6]
    vec_c = [1, 0, 0]
    print(f"ab: {cosine_similarity(vec_a, vec_b)}")  # 0.9746318461970762
    print(f"ac: {cosine_similarity(vec_a, vec_c)}")  #0.2672612419124244
    print(f"bc: {cosine_similarity(vec_b, vec_c)}")  #0.4558423058385518   